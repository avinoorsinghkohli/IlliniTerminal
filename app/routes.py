from flask import Flask, request, jsonify, abort
import os
from openai import OpenAI
from agent.basic_llm import get_answer
from agent.clients import create_client
import helper
from agent.query_generator import get_query_list
from agent.stack_overflow_checker import fetch_context_for_query, generate_fix_with_llm
from dotenv import load_dotenv

load_dotenv('../env')

app = Flask(__name__)

llm_client = create_client('openai', os.getenv('OPENAI_API_KEY'))

generated_fixes_store = []

def generate_llm_response(query):
    formatted_query = f"""
    {query}

    **Format the response strictly in markdown.**
    """
    generated_text = get_answer(formatted_query, llm_client, 'gpt-4o-mini')

    generated_fixes_store.append(generated_text)

    return generated_text


@app.route('/generate', methods=['GET'])
def generate():
    try:
        error_file_path = request.args.get('error_file', '')

        if not error_file_path:
            abort(400, 'error_file parameter is required')

        if not os.path.exists(error_file_path):
            abort(400, 'Error file does not exist')

        with open(error_file_path, 'r', encoding='utf-8') as error_file:
            error_log = error_file.read()

        error_files = helper.extract_java_files(error_log)
        code_files = {}

        for error_file in error_files:
            if os.path.exists(error_file):
                with open(error_file, 'r', encoding='utf-8') as code_file:
                    code_files[error_file] = code_file.read()
            else:
                print(f"File {error_file} does not exist.")

        queries = get_query_list(error_log)
        print(queries)
        # test_query = queries[0]

        context = None

        while not context:
            for query in queries:
                context = fetch_context_for_query(query)
                if context:
                    break

        print("CONTEXT", context)

        global generated_fixes_store
        generated_fixes_store = []

        if context:
            generated_fix = generate_fix_with_llm(llm_client, error_log, context, code_files)
            generated_fixes_store.append(generated_fix)
            print("Generated Fix:\n", generated_fix)
        
        if not generated_fix:
            return jsonify({'error': 'No fix generated'}), 400
        
        return generated_fix

    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500


@app.route('/retry', methods=['GET'])
def retry():
    global generated_fixes_store
    try:
        if not generated_fixes_store:
            return jsonify({'error': 'No previous generated fix available'}), 400

        error_file_path = request.args.get('error_file', '')

        if not error_file_path:
            abort(400, 'error_file parameter is required')

        if not os.path.exists(error_file_path):
            abort(400, 'Error file does not exist')

        with open(error_file_path, 'r', encoding='utf-8') as error_file:
            error_log = error_file.read()

        error_files = helper.extract_java_files(error_log)
        code_files = {}

        for error_file in error_files:
            if os.path.exists(error_file):
                with open(error_file, 'r', encoding='utf-8') as code_file:
                    code_files[error_file] = code_file.read()
            else:
                print(f"File {error_file} does not exist.")

        previous_solution = generated_fixes_store[-1]

#         retry_query = f"""
#         ## Code:
#         ```
#         {code_files}
#         ```

# #         ## Error Log:
# #         ```
# #         {error_log}
# #         ```

# #         **Suggest the top 2 fixes as part of the corrected code.**
# #         """

        # generated_text = get_answer(query, llm_client, 'gpt-4o-mini')
        # # generated_text = "SUCCESS"
        # return jsonify({'response': generated_text})

        queries = get_query_list(error_log)
        print(queries)
        # test_query = queries[0]

        context = None

        while not context:
            for query in queries:
                context = fetch_context_for_query(query)
                if context:
                    break
        print(context)

        if context:
            generated_fix = generate_fix_with_llm(llm_client, error_log, context, code_files, previous_fixes = previous_solution)
            generated_fixes_store.append(generated_fix)
            print("Generated Fix:\n", generated_fix)
        
        return generated_fix

    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)