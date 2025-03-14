# This is a simple example of using Python HTTP library to send POST requests to call the GPT API.
#——————————————————————————————————————————————————————————————————
# Python environment needs to install python-dotenv openai
# !pip install python-dotenv openai
# !pip install --upgrade openai
# Additionally, you need to configure the .env file, which needs to specify OPENAI_API_KEY and OPENAI_BASE_URL
""" By default, Python reads files using the default encoding of Windows, which is gbk.
However, modern documents are generally in utf-8 format. Therefore, Python needs to be set to utf-8 mode.
You can search for environment variables, then configure the environment variable PYTHONUTF8, with a value of 1. """
#——————————————————————————————————————————————————————————————————
modelname = "gpt-3.5-turbo"

import os
import requests
import json

# Load .env file into environment variables
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

"""
Content-Type: Specifies the type of request data being sent, common values include:
text/plain: Plain text data
application/x-www-form-urlencoded: Data passed through page forms (HTML <form> tag)
application/json: JSON formatted data 
application/xml: XML formatted data

Authorization: Authentication information carried in the request. For example, most model APIs, especially OpenAI-Like format model interfaces, use Bearer Token authentication by placing the API-Key in this request header, e.g.: Authorization: Bearer sk-xxxxxxxx
"""

response = requests.post(
    f"{os.environ['OPENAI_BASE_URL']}/chat/completions",
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer { os.environ['OPENAI_API_KEY'] }",
    },
    json={
        "model": modelname, # "gpt-4o-mini"
        "messages": [
        {
            "role": "developer",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": "Hello!"
        }
        ],
    },
)
print(response.status_code)
"""
200 OK: Request successful, server returns requested data.
201 Created: Request successful and resource created (common for POST requests).
400 Bad Request: Request format error, server cannot understand.
401 Unauthorized: Request not authorized, may lack valid authentication.
404 Not Found: Requested resource does not exist.
429 Too Many Requests: Request exceeds rate limit.
500 Internal Server Error: Server error, unable to process request.
"""
print()
print(response.content)
print()
response_data = json.loads(response.content.decode())
print(response_data)
print()
print(response_data["choices"][0]["message"])