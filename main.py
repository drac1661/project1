from fastapi import FastAPI, HTTPException, Query
import os
import subprocess
import re
import json
from typing import Optional, List
import requests

from tasks import (
    install_and_run_datagen,
    format_file,
    count_wednesdays,
    sort_contacts,
    recent_logs,
    create_index,
    extract_email,
    extract_credit_card,
    find_similar_comments,
    calculate_gold_sales,
    # Import additional Phase B task functions here
)

app = FastAPI()

DATA_DIR = "/data"
AIPROXY_TOKEN = os.getenv("AIPROXY_TOKEN")
host = os.getenv("HOST")  # Replace with actual LLM endpoint

# Task mapping
task_mapping = {
    "A1": install_and_run_datagen,
    "A2": format_file,
    "A3": count_wednesdays,
    "A4": sort_contacts,
    "A5": recent_logs,
    "A6": create_index,
    "A7": extract_email,
    "A8": extract_credit_card,
    "A9": find_similar_comments,
    "A10": calculate_gold_sales,
    # Add Phase B task mappings here
}

# def validate_path(path: str):
#     """Ensure the path is within the /data directory."""
#     if not os.path.abspath(path).startswith(os.path.abspath(DATA_DIR)):
#         raise HTTPException(status_code=400, detail="Access to paths outside /data is restricted")

def call_llm(task_description: str) -> dict:
    """Call the LLM to parse the task description."""
    headers = {
        "Authorization": f"Bearer {AIPROXY_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "gpt-4o-mini",  # Ensure this matches the supported model
        "messages": [
            {"role": "system", "content": """You are an automation agent that parses plain-English task descriptions and maps them to predefined tasks (A1 to A10). Given a task description, output a JSON object with a "tasks" key, which contains a list of tasks to execute. Each task should include a "name" corresponding to the task identifier (e.g., "A2") and a "params" object containing the required parameters. so Identify which predefined task (A1 to A10) matches this user input and respond with only the task code.Classify the following task into one of these categories:
                                A1: generate_data
                                A2: format_file
                                A3: count_dates
                                A4: sort_contact_json
                                A5: process_logs
                                A6: find_all_markdown
                                A7: extract_email
                                A8: credit_card_process_image
                                A9: find_similar_comments
                                A10: query_database
            return the required params  and in params when the name is A3 then give the "input_file" key and "output_file" key and "day" key otherwise give only "input_file" key and "output_file" key"
                                
                                """
                                },
            
            {"role": "user", "content": f"{task_description}"},
        ],
    }

    try:
        response = requests.post(host, headers=headers, json=payload, timeout=15)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error communicating with LLM: {str(e)}")

@app.post("/run")
def run_task(task: str = Query(..., description="Plain English task description")):
    """Processes the task using an LLM and executes the corresponding action."""
    try:
        # Call the LLM to parse the task
        llm_response = call_llm(task)
        print("Raw LLM response:", llm_response)
        
        completion = llm_response.get("choices", [{}])[0].get("message", {}).get("content", "")
        print(completion)
        if not completion.strip():
            raise HTTPException(status_code=500, detail="Empty response from LLM")
        
        completion = re.sub(r"^```json\n|\n```$", "", completion.strip())
        
        try:
            instructions = json.loads(completion)
            print(instructions)
        except json.JSONDecodeError as e:
            raise HTTPException(status_code=500, detail=f"Invalid JSON: {str(e)}")

        
        results = []
        for instr in instructions.get("tasks", []):
            task_name = instr.get("name")
            params = instr.get("params", {})

            if task_name in task_mapping:
                func = task_mapping[task_name]
            print(params)
            result = func(**params)
            
            results.append({task_name: result})
            print(result)
            # if isinstance(input_file, str):
            #     validate_path(input_file)

            #     result = func(**params)
            #     results.append({task_name: result})
            # else:
            #     raise HTTPException(status_code=400, detail=f"Unknown task name: {task_name}")
        
        return {"status": "success", "results": results}
    
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid JSON response from LLM")
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/read")
def read_file(path: str = Query(..., description="File path")):
    """Reads and returns the content of the specified file."""
    # validate_path(path)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File not found")
    with open(path, "r") as f:
        return {"content": f.read()}