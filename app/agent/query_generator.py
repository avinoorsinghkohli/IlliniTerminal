from typing import List
from pydantic import BaseModel, Field
import os
import getpass
from dotenv import load_dotenv
load_dotenv()
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain.chains import LLMChain

if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter API key for OpenAI: ")

class Query(BaseModel):
    """A search query."""
    query: str = Field(description="The query to search for")

class QueryList(BaseModel):
    """List of queries extracted from the error message."""
    queries: List[Query]

# KEYWORD_EXTRACTOR_PROMPT = """You are a query generator. 
# You are given an error message from any programming language and you have to use the error message to create a Python list of search queries that will be useful in searching Stack Overflow for relevant solutions.
# Make every query in the list as concise as possible, but do not omit important search terms. 
# Output MUST be a python list with every element enclosed with double quotes.
# ERROR: {error_message}"""

KEYWORD_EXTRACTOR_PROMPT = """You are a query generator. 
You are given an error message from any programming language and you have to use the error message to create a Python list of search queries that will be useful in searching Stack Overflow for relevant solutions.
Find the exact error line, extract it and return that as the 1st query.
Output MUST be a python list with every element enclosed with double quotes.
ERROR: {error_message}"""

# Initialize the base LLM
llm = init_chat_model("gpt-4o-mini", model_provider="openai")

# Wrap it with a structured output schema
structured_llm = llm.with_structured_output(schema=QueryList)

def get_query_list(error_message: str) -> List[str]:
    """
    Given an error message, return a list of query strings 
    that can be used to search for solutions on Stack Overflow.
    """
    # Format the prompt with the user-provided error message
    formatted_prompt = KEYWORD_EXTRACTOR_PROMPT.format(error_message=error_message)
    
    # Invoke the LLM and parse the result into the QueryList pydantic model
    result_obj = structured_llm.invoke(formatted_prompt)
    
    # Extract and return the raw query strings
    return [q.query for q in result_obj.queries]





# from typing import List, Optional
# from pydantic import BaseModel, Field
# import os
# from dotencv import load_dotenv
# load_dotenv()
# from langchain.chat_models import init_chat_model
# from langchain_openai import ChatOpenAI
# import getpass
# from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
# from langchain.chains import LLMChain

# if not os.environ.get("OPENAI_API_KEY"):
#   os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter API key for OpenAI: ")

# class Query(BaseModel):
#     """A search query."""
#     query: str = Field(default="", description="The query to search for")

# class QueryList(BaseModel):
#     """Extracted data about people."""
#     queries: List[Query]
# KEYWORD_EXTRACTOR_PROMPT = """You are a query generator. You are given a an error message from any programming language. You have to use the error message to create a python list of search queries that will be useful in conducting a search in stack-overflow to find a solution to the error.\ 
# Make every query in the list as short as possible. Having less words will produce better results. But make sure you do not omit important search terms and make the search query too general. It does not have to be a complete sentence. 
# Output MUST be a python list with every element enclosed with double quotes. 
# ERROR: {error_message}"""




# llm = init_chat_model("gpt-4o-mini", model_provider="openai")
# structured_llm = llm.with_structured_output(schema=QueryList)


# prompt_template = ChatPromptTemplate([
#     ("system", "You are a helpful assistant"),
#     ("user", KEYWORD_EXTRACTOR_PROMPT)
# ])

# keyword_extractor = LLMChain(
#         llm=llm,
#         prompt=PromptTemplate.from_template(KEYWORD_EXTRACTOR_PROMPT)
#     )

# prompt=PromptTemplate.from_template(KEYWORD_EXTRACTOR_PROMPT)




#     # Creates a model so that we can extract multiple entities.
#     people: List[Query]


# def get query_list(text: str) -> List[str]:



# prompt = prompt_template.invoke({"text": text})
# structured_llm.invoke(prompt)

# # text = "My name is Jeff, my hair is black and i am 6 feet tall. Anna has the same color hair as me."
# # prompt = prompt_template.invoke({"text": text})
# # structured_llm.invoke(prompt)