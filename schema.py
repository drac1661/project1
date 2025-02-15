function_descriptions = [
    {
        "name": "ask_openai",
        "description": "Send a question and context to OpenAI API and return the response.",
        "parameters": {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "description": "The prompt or question to send to the OpenAI API."
                }
            },
            "required": ["prompt"],
        },
    },
    {
        "name": "emailsender",
        "description": "Extract the sender's email address from the email content.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
    {
        "name": "contactsort",
        "description": "Sort contacts by last name and first name.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
    {
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
            "required": ["text"],
        },
    },
    {
        "name": "embedding",
        "description": "Compute embeddings for comments and find the most similar pair.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
    {
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
            "required": ["image_path"],
        },
    },
    {
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
            "required": ["base64_image", "prompt"],
        },
    },
    {
        "name": "detect_image",
        "description": "Detect and extract information from an image.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
    {
        "name": "log",
        "description": "Read the most recent log files and write the first line of each to a new file.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
    {
        "name": "markdownn",
        "description": "Create an index of Markdown files based on their H1 headers.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
    {
        "name": "sqlitte",
        "description": "Calculate total sales for 'Gold' ticket type from a SQLite database.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
    {
        "name": "whichday",
        "description": "Count how many Wednesdays are in a list of dates.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
]