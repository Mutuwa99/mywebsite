from flask import Flask, render_template, request, jsonify
from difflib import get_close_matches
import json
import random

app = Flask(__name__)

# Load the knowledge base from a JSON file
def load_knowledge_base(file_path: str):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Save the updated knowledge base to the JSON file
def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

# Load the knowledge base
knowledge_base = load_knowledge_base('knowledge_base.json')

# Route for the chatbot frontend
@app.route('/')
def index():
    return render_template('base.html')

# API endpoint to handle user input and respond
@app.route('/chatbot', methods=['POST'])
def chatbot():
    user_input = request.json['message']

    if user_input.lower() == 'quit':
        return jsonify({'answer': 'Goodbye!'})

    # Iterate through intents in the knowledge base
    for intent in knowledge_base['intents']:
        # Check if user input matches any patterns in the current intent
        if any(pattern.lower() in user_input.lower() for pattern in intent['patterns']):
            # Select a random response from the intent's responses
            response = random.choice(intent['responses'])
            return jsonify({'answer': response})

    # If the chatbot doesn't know the answer, prompt the user to teach it
    response = 'I don\'t know the answer. Can you please teach me?'

    # Check if the user wants to teach the chatbot
    if 'yes' in user_input.lower():
        # Extract the user input and response from the message
        parts = user_input.split(':', 1)
        question_parts = parts[1].split('.', 1)
        question = question_parts[0].strip()
        response = question_parts[1].strip()

        # Find the existing intent, if any, that matches the question
        existing_intent = next(
            (intent for intent in knowledge_base['intents'] if question in intent['patterns']), None
        )

        if existing_intent:
            existing_intent['responses'].append(response)
        else:
            # Create a new intent with the provided question and response
            new_intent = {
                'tag': 'new',
                'patterns': [question],
                'responses': [response]
            }
            knowledge_base['intents'].append(new_intent)

        # Save the updated knowledge base to the file
        save_knowledge_base('knowledge_base.json', knowledge_base)

        response = 'Thank you for teaching me!'

    return jsonify({'answer': response})

# Run the Flask application
if __name__ == '__main__':
    app.run()
