import os
from flask import Flask, render_template, request
import requests
import json
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Define the ChatGPT API endpoint
API_ENDPOINT = "https://api.openai.com/v1/chat/completions"

# Retrieve the API key from an environmental variable
API_KEY = os.getenv("OPENAI_API_KEY")

# Render the index.html template
@app.route('/')
def index():
    return render_template('index.html')

# Handle user input and make a request to the ChatGPT API
@app.route('/get_response', methods=['POST'])
def get_response():
    # Retrieve user input from the frontend
    user_input = request.form['user_input']

    # Make a request to the ChatGPT API
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + API_KEY
    }
    data = {
        'model': 'gpt-3.5-turbo',
        'messages': [{'role': 'system', 'content': 'You are a helpful assistant.'},
                     {'role': 'user', 'content': user_input}]
    }
    response = requests.post(API_ENDPOINT, headers=headers, json=data)

    if response.ok:
        response_data = response.json()
        model_reply = response_data['choices'][0]['message']['content'] if 'choices' in response_data else 'Oops! Something went wrong.'
    else:
        model_reply = 'Oops! Something went wrong. Error: {}'.format(response.text)

    # Return the model's reply to the frontend
    return model_reply

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)
