import os
import json

# Define the directory containing the Markdown files
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
