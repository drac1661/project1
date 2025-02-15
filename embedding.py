import requests
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import os

# OpenAI API Key
api_key = os.getenv("API_KEY") # Set your OpenAI API key

# Step 1: Read comments from file


# Step 2: Generate embeddings for comments using requests
def get_embedding(text):
    print("a")
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


