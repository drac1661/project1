import base64
from dotenv import load_dotenv
load_dotenv()
import os
import json
import requests

api_key=os.getenv("API_KEY")
host=os.getenv("HOST")




# Function to encode the image
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


