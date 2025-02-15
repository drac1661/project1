from dotenv import load_dotenv
load_dotenv()
import os
import json
import requests

api_key=os.getenv("API_KEY")
host=os.getenv("HOST")

def ask_openai(prompt):
    """Send a question and context to OpenAI API and return the response."""
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    data = {
        'model': 'gpt-4-turbo',  
        'messages': [
            {'role': 'user', 'content': prompt}
        ]
    }
    
    response = requests.post(host, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f"Error: {response.status_code}, {response.text}"
    
def emailsender():
    with open('data/email.txt', 'r') as file:
        email_content = file.read()

    prompt=f"{email_content} give only the sender's email address"
    email_ad=ask_openai(prompt)
    with open('data/email-sender.txt','w') as f:
        f.write(email_ad)

