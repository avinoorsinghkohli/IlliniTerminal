import faiss
import numpy as np
import requests
from sentence_transformers import SentenceTransformer
from bs4 import BeautifulSoup
from openai import OpenAI
from pydantic import BaseModel

class Insertion(BaseModel):
    line_number: int
    new_lines: list[str]

class Modification(BaseModel):
    line_number: int
    modified_line: str

class Patch(BaseModel):
    file_path: str
    insertions: list[Insertion]
    deletions: list[int]
    modifications: list[Modification]

class FixResponse(BaseModel):
    fixes: list[Patch]



embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
# client = OpenAI(api_key=api_key)
def clean_html(raw_html):
    return BeautifulSoup(raw_html, "html.parser").get_text()

def generate_embedding(text):
    return embedding_model.encode([text])[0]

def search_stackoverflow(query, max_questions=5):
    url = "https://api.stackexchange.com/2.3/search"
    params = {
        'order': 'desc',
        'sort': 'votes',
        'intitle': query,
        'site': 'stackoverflow',
        'pagesize': max_questions
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json().get('items', [])

def get_answers(question_id, max_answers=5):
    url = f"https://api.stackexchange.com/2.3/questions/{question_id}/answers"
    params = {
        'order': 'desc',
        'sort': 'votes',
        'site': 'stackoverflow',
        'filter': 'withbody',
        'pagesize': max_answers
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json().get('items', [])

def build_faiss_index(questions):
    dimension = 384
    index = faiss.IndexFlatL2(dimension)
    
    question_texts = []
    question_embeddings = []

    for question in questions:
        text = question['title']
        embedding = generate_embedding(text)
        index.add(np.array([embedding], dtype=np.float32))
        question_texts.append(text)
        question_embeddings.append(embedding)

    return index, question_texts, question_embeddings

def find_top_matches(query, index, question_texts, top_k=2):
    query_embedding = generate_embedding(query)
    _, indices = index.search(np.array([query_embedding], dtype=np.float32), top_k)
    return [question_texts[i] for i in indices[0]]

def fetch_context_for_query(query):
    questions = search_stackoverflow(query)
    
    if not questions:
        return "No relevant questions found."

    index, question_texts, _ = build_faiss_index(questions)
    top_matches = find_top_matches(query, index, question_texts)

    context = []
    for question in questions:
        if question['title'] in top_matches:
            answers = get_answers(question['question_id'])
            clean_answers = [clean_html(ans['body']) for ans in answers]
            context.extend(clean_answers)

    return "\n\n".join(context[:5])

def generate_fix_with_llm(client, error_message, so_context, error_files, previous_fixes = None):
    prompt = f"""
Error message:
"{error_message}"
"""

    if error_files:
        prompt += f"""
Error files:
"{error_files}"
"""

    prompt += f"""
Stack Overflow solution suggestions:
{so_context}

Find the best possible fixes for the issue, ensuring correctness and clarity. Don't give any irrelevant suggestions.

"""
    if previous_fixes:
        prompt += f"""
Here are the previous fixes attempted that did not work, do not repeat these mistakes:

"{previous_fixes}"
"""

    messages = [
        {"role": "system", "content": """You are an expert software developer. 
Task: Given an error message, the files relating to the error(optional), and Stack Overflow suggestions, you need to generate an accurate code fix for the error. Note that there may be multiple errors in the code. Handle them all.
Give the best solution in a well structured and concise manner. You need only to mention the edits required (with line numbers if code files are provided), not the entire updated code.
Output format: You need to reply using well formatted Markdown with nice colors."""},
        {"role": "user", "content": prompt}
    ]
    completion = client.chat(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.1
    )
    # print(completion)
    return completion

if __name__ == "__main__":
    so_context = fetch_context_for_query("Spring Boot Configuration not found")
    print(so_context)