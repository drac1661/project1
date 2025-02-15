from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import json
import subprocess
from dotenv import load_dotenv
import os
load_dotenv()

app=FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['GET','POST'],
    allow_headers=['*']
)

tools=[
    {
    "type": "function",
    "function": {
        "name": "script_runner",
        "description": "Install a package and run a script from a URL with provided arguments.",
        "parameters": {
            "type": "object",
            "properties": {
                "script_url": {
                    "type": "string",
                    "description": "The URL of the script to run"
                },
                "args": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "List of arguments to pass to the script"
                }
            },
            "required": ["script_url", "args"]
        }
    }
},
{
        "type": "function",
        "function": {
            "name": "emailsender",
            "description": "Extract the sender's email address from the email content.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "contactsort",
            "description": "Sort contacts by last name and first name.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_embedding",
            "description": "Get the embedding of a given text using the OpenAI API.",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The text to get the embedding for."
                    }
                },
                "required": ["text"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "embedding",
            "description": "Compute embeddings for comments and find the most similar pair.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "encode_image",
            "description": "Encode an image to a base64 string.",
            "parameters": {
                "type": "object",
                "properties": {
                    "image_path": {
                        "type": "string",
                        "description": "The path to the image file to encode."
                    }
                },
                "required": ["image_path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "image_to_textbase64",
            "description": "Send a base64 encoded image to the OpenAI API and get a response.",
            "parameters": {
                "type": "object",
                "properties": {
                    "base64_image": {
                        "type": "string",
                        "description": "The base64 encoded image string."
                    },
                    "prompt": {
                        "type": "string",
                        "description": "The prompt to send along with the image."
                    }
                },
                "required": ["base64_image", "prompt"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "detect_image",
            "description": "Detect and extract information from an image.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "log",
            "description": "Read the most recent log files and write the first line of each to a new file.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "markdownn",
            "description": "Create an index of Markdown files based on their H1 headers.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "sqlitte",
            "description": "Calculate total sales for 'Gold' ticket type from a SQLite database.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "whichday",
            "description": "Count how many Wednesdays are in a list of dates.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }
]



app.get("/")
def home():
    return {"runing"}, 200

@app.get('/read')
def read_file(path:str):
    try:
        with open(path,"r") as f:
            return f.read()
    except Exception as e:
        raise HTTPException(status_code=404,details="file doesn't exits")
    



APIPROXY_TOKEN=os.getenv("APIPROXY_TOKEN")

@app.post('/run')
def task_runner(task:str):
    url="https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
    data={
        "model":"gpt-4o-mini",
        "messages":[
            {
                "role":"user",
                "content":task,

            },
            {
                "role":"system",
                "content":""""
                you are an assistant who has to do variety of tasks if your task involves running  a script , you can use the script_runner tool. 
                If your task involves writing a code you can use the task_runner tool.
                """
            }
        ],
        "tools":tools
    }
    headers={
        "content-type":'application/json',
        "Authorization":f'Bearer {APIPROXY_TOKEN}'

    }
    response=requests.post(url=url,headers=headers, json=data,verify=False)
    arguments= response.json()['choices'][0]['message']['tool_calls'][0]['function']['arguments']
    script_url=json.loads(arguments)['script_url']
    email=json.loads(arguments)['args'][0]
    command =["uv","run",script_url,email]
    subprocess.run(command)
    return response.json()







if __name__ =="__main__":
    import uvicorn
    uvicorn.run(app,host='0.0.0.0' , port=8080)



