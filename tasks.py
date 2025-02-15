import json
import numpy as np
import sqlite3
import os
import subprocess
import glob
import pytesseract
import re
from PIL import Image
from datetime import datetime
from sentence_transformers import SentenceTransformer, util

# Load transformer model for text similarity
model = SentenceTransformer("all-MiniLM-L6-v2")

# A1 - Install uv and run datagen.py
def install_and_run_datagen(email):
    try:
        subprocess.run(["pip", "install", "uvicorn"], check=True)
        subprocess.run(["python", "https://raw.githubusercontent.com/sanand0/tools-in-data-science-public/tds-2025-01/project-1/datagen.py", email], check=True)
        return f"datagen.py executed with email: {email}"
    except subprocess.CalledProcessError as e:
        raise Exception(f"Error executing datagen.py: {e}")

# A2 - Format a file using Prettier
def format_file(input_file,output_file):
            command = ["cmd", "/c", "npx", "prettier@3.4.2", "--write", input_file]
            print(f"Executing command: {' '.join(command)}")
            subprocess.run(command, check=True)

# A3 - Count Wednesdays in a file
def count_wednesdays(input_file: str, output_file: str, day: str):
    """Counts occurrences of a specific day in a list of dates and writes the result to a file."""
    
    # List of supported date formats
    date_formats = ["%Y-%m-%d", "%d-%b-%Y", "%b %d, %Y", "%Y/%m/%d %H:%M:%S"]

    try:
        weekday_index = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"].index(day)
    except ValueError:
        raise ValueError(f"Invalid day name: {day}. Use a valid day like 'Monday', 'Tuesday', etc.")

    with open(input_file, "r", encoding="utf-8") as f:
        dates = f.readlines()

    def parse_date(date_str):
        """Try multiple formats until one works."""
        for fmt in date_formats:
            try:
                return datetime.strptime(date_str.strip(), fmt)
            except ValueError:
                continue
        raise ValueError(f"Date format not recognized: {date_str.strip()}")

    # Count occurrences of the specified day
    day_count = sum(1 for date in dates if parse_date(date).weekday() == weekday_index)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(str(day_count))

    return f"{day} count written to {output_file}"

# A4 - Sort contacts.json by last and first name
def sort_contacts(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as f:
        contacts = json.load(f)

    sorted_contacts = sorted(contacts, key=lambda x: (x["last_name"], x["first_name"]))

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(sorted_contacts, f, indent=4)

    return f"Contacts sorted and saved to {output_file}"

# A5 - Find 10 most recent logs
def recent_logs(input_file, output_file):
    log_files = glob.glob(os.path.join(input_file, "*.log"))
    log_files.sort(key=os.path.getmtime, reverse=True)  # Sort by most recent

    recent_lines = []
    for log_file in log_files[:10]:
        with open(log_file, "r", encoding="utf-8") as f:
            first_line = f.readline().strip()
            recent_lines.append(first_line)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(recent_lines))

    return f"Saved first lines of the 10 most recent logs to {output_file}"



# A6 - Create Index
def create_index(input_file, output_file):
    # Dictionary to store file-title mappings
    index = {}

    # Get all .md files recursively
    md_files = glob.glob(os.path.join(input_file, "**/*.md"), recursive=True)

    for md_file in md_files:
        title = None
        with open(md_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("# "):  # First H1 title found
                    title = line[2:].strip()  # Remove "# " and leading/trailing spaces
                    break
        
        if title:  # If an H1 was found, store it
            relative_path = os.path.relpath(md_file, input_file)  # Remove /data/docs/ prefix
            index[relative_path] = title

    # Save index to JSON
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=4)

    print(f"Index file created at {output_file}")



#  A7   -  find sender mail
def extract_email(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as f:
        email_content = f.read()

    # Extract sender email using regex
    match = re.search(r'From: ".*?" <(.*?)>', email_content)

    if match:
        sender_email = match.group(1)
        
        # Write to output file
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(sender_email)

        print(f"Sender email extracted: {sender_email}")
    else:
        print("No sender email found.")

# A8 - Extract credit card number from an image
def extract_credit_card(input_file, output_file):
    image = Image.open(input_file)

    # Perform OCR to extract text
    extracted_text = pytesseract.image_to_string(image)

    # Find the credit card number (a 16-digit sequence)
    match = re.search(r"\b\d{8} \d{7}\b", extracted_text)

    if match:
        credit_card_number = match.group().replace(" ", "")  # Remove spaces
        # Write to file
        with open(output_file, "w") as f:
            f.write(credit_card_number)
        print(f"Credit card number extracted and saved to {output_file}")
    else:
        print("No credit card number found.")
    
    
# A9 - Find the most similar pair of comments
def find_similar_comments(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        comments = f.readlines()

    comments = [comment.strip() for comment in comments if comment.strip()]
    embeddings = model.encode(comments, convert_to_tensor=True)
    cosine_scores = util.pytorch_cos_sim(embeddings, embeddings)
    np.fill_diagonal(cosine_scores.numpy(), -1)
    max_sim_indices = np.unravel_index(np.argmax(cosine_scores.numpy()), cosine_scores.shape)
    most_similar_comments = (comments[max_sim_indices[0]], comments[max_sim_indices[1]])

    with open(output_file, 'w', encoding='utf-8') as f:
        for comment in most_similar_comments:
            f.write(comment + '\n')

    return "Most similar comments written to data/comments-similar.txt"

# A10 - Calculate total sales for "Gold" tickets
def calculate_gold_sales(input_file, output_file):
    conn = sqlite3.connect(input_file)
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(units * price) FROM tickets WHERE type='Gold'")
    total_sales = cursor.fetchone()[0] or 0

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(str(total_sales))

    conn.close()
    return f"Total sales for 'Gold' tickets written to {output_file}"

# Additional Phase B tasks (B3-B10) can be added here similarly