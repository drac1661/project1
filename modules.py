import json
import os
import requests
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import base64
import glob
import sqlite3
from datetime import datetime
import subprocess



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


def contactsort():
    with open('data/contacts.json', 'r') as file:
        contacts = json.load(file)

    # Step 2: Sort the contacts by last_name, then first_name
    sorted_contacts = sorted(contacts, key=lambda contact: (contact['last_name'], contact['first_name']))

    # Step 3: Write the sorted contacts to contacts-sorted.json
    with open('data/contacts-sorted.json', 'w') as file:
        json.dump(sorted_contacts, file, indent=4)

def get_embedding(text):
    url = "https://llmfoundry.straive.com/v1/embeddings"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "text-embedding-ada-002",
        "input": text
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()['data'][0]['embedding']
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None
    

def embedding():
    with open('data/comments.txt', 'r') as file:
        comments = file.readlines()
    # Get embeddings for all comments
    embeddings = [get_embedding(comment.strip()) for comment in comments]

    # Step 3: Compute pairwise cosine similarities
    similarity_matrix = cosine_similarity(embeddings)

    # Step 4: Find the most similar pair of comments
    max_similarity = -1
    most_similar_pair = (None, None)

    for i in range(len(comments)):
        for j in range(i + 1, len(comments)):
            if similarity_matrix[i][j] > max_similarity:
                max_similarity = similarity_matrix[i][j]
                most_similar_pair = (comments[i], comments[j])

    # Step 5: Write the most similar pair to a file
    with open('data/comments-similar.txt', 'w') as file:
        file.write(most_similar_pair[0].strip() + '\n')
        file.write(most_similar_pair[1].strip() + '\n')


def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def image_to_textbase64(base64_image,prompt):
  
    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
    }

    payload = {
    "model": "gpt-4o-mini",
    "messages": [
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": "give number of person holding stick in the image give only number"
            },
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
            }
            }
        ]
        }
    ],
    "max_tokens": 300
    }

    response = requests.post("https://llmfoundry.straive.com/openai/v1/chat/completions", headers=headers, json=payload)

    
    data=response.json()
    # category=data.choices[0].message.content
    return (data['choices'][0]['message']['content'])


def detect_image():
    image_path = f"data/credit-card.png"
    base64_image = encode_image(image_path)
    prompt="give only the card number without space"
    card_number=image_to_textbase64(base64_image,prompt)
    with open('data/credit-card.txt','w') as f:
       f.write(card_number)


def log():
    log_directory = 'data/logs/'
    output_file = 'data/logs-recent.txt'
    log_files = glob.glob(os.path.join(log_directory, '*.log'))

    log_files.sort(key=os.path.getmtime, reverse=True)
    lines_to_write = []
    for log_file in log_files[:10]:  # Limit to the 10 most recent files
        with open(log_file, 'r') as file:
            first_line = file.readline().strip()  # Read the first line
            lines_to_write.append(first_line)

    with open(output_file, 'w') as output:
        for line in lines_to_write:
            output.write(line + '\n')

def markdownn():
    docs_directory = 'data/docs/'
    index_file_path = os.path.join(docs_directory, 'index.json')

    # Initialize a dictionary to hold the index
    index = {}

    # Walk through the directory to find all .md files
    for root, dirs, files in os.walk(docs_directory):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                # Open the Markdown file and read its contents
                with open(file_path, 'r', encoding='utf-8') as f:
                    # Read lines and find the first H1 header
                    for line in f:
                        if line.startswith('# '):  # H1 header starts with '# '
                            title = line[2:].strip()  # Extract the title (remove '# ')
                            # Store the filename (without the prefix) and title in the index
                            index[file] = title
                            break  # Stop after the first H1 header

    # Write the index to a JSON file
    with open(index_file_path, 'w', encoding='utf-8') as index_file:
        json.dump(index, index_file, indent=4)


def sqlitte():
    # Connect to the SQLite database
    db_path = 'data/ticket-sales.db'
    conn = sqlite3.connect(db_path)

    # Create a cursor object
    cursor = conn.cursor()

    # Query to calculate total sales for "Gold" ticket type
    query = """
    SELECT SUM(units * price) AS total_sales
    FROM tickets
    WHERE type = 'Gold';
    """

    # Execute the query
    cursor.execute(query)

    # Fetch the result
    result = cursor.fetchone()

    # Get the total sales value
    total_sales = result[0] if result[0] is not None else 0

    # Write the total sales to a text file
    output_path = 'data/ticket-sales-gold.txt'
    with open(output_path, 'w') as file:
        file.write(str(total_sales))

    # Close the cursor and connection
    cursor.close()
    conn.close()


def whichday():
    input_file_path = 'data/dates.txt'
    output_file_path = 'data/dates-wednesdays.txt'

    wednesday_count = 0

    date_formats = [
        "%b %d, %Y",  # Oct 31, 2005
        "%d-%b-%Y",    # 30-Mar-2010
        "%Y-%m-%d",    # 2018-03-03
        "%b %d, %Y",   # Dec 23, 2024
        "%b %d, %Y",   # Mar 19, 2009
        "%Y/%m/%d %H:%M:%S"  # 2008/07/27 19:12:56
    ]

    # Read the dates from the input file
    with open(input_file_path, 'r') as file:
        for line in file:
            date_str = line.strip()
            for date_format in date_formats:
                try:
                    # Try to parse the date
                    date_obj = datetime.strptime(date_str, date_format)
                    # Check if the date is a Wednesday (0 = Monday, ..., 2 = Wednesday)
                    if date_obj.weekday() == 2:
                        wednesday_count += 1
                    break  # Exit the loop if parsing was successful
                except ValueError:
                    continue  # Try the next format if parsing fails

    with open(output_file_path, 'w') as output_file:
        output_file.write(str(wednesday_count))

def format_markdown():
    file_path='data/format.md'
    if not os.path.isfile(file_path):
       return f"File not found: {file_path}"
    try:
        subprocess.run(['prettier', '--write', file_path], check=True)
    except subprocess.CalledProcessError as e:
        return f"Error formatting file: {e}"




