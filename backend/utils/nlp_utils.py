from utils.rag_utils import retrieve_documents
import requests
import os
import openai

# Load your OpenAI API key from the environment
openai.api_key = os.environ.get('OPENAI_API_KEY')

def call_openrouter_api(prompt, max_length=200):
    api_url = 'https://openrouter.ai/api/v1/chat/completions'
    
    headers = {
        'Authorization': f'Bearer {openai.api_key}',
        'Content-Type': 'application/json'
    }

    data = {
        'model': 'openai/gpt-4o-mini', 
        'messages': [
            {"role": "system", "content": "You are a helpful AI math tutor."},
            {"role": "user", "content": prompt}
        ],
        'max_tokens': max_length,
        'temperature': 0.7 
    }

    response = requests.post(api_url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        raise Exception(f"OpenRouter API error: {response.status_code} - {response.text}")

def generate_explanation(problem_id, retrieved_documents):
    # Retrieve the original problem statement based on problem_id 
    problem_statement = get_problem_statement(problem_id)

    context = "\n\n".join([doc['content'] for doc in retrieved_documents])

    prompt = f"Explain the solution to the following math problem, considering the provided context:\n\nProblem:\n{problem_statement}\n\nContext:\n{context}"

    explanation = call_openrouter_api(prompt)

    return explanation

# Function to retrieve the problem statement (implementation depends on your quiz data structure)
def get_problem_statement(problem_id):
    # Assuming you have a global `quiz_data` dictionary in math_utils.py
    from utils.math_utils import quiz_data 

    # Find the question with the matching ID
    for question in quiz_data.get('questions', []):
        if question['id'] == problem_id:
            return question['question']

    # If no matching question is found, return a default message
    return "Problem statement not found."