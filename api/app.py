from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests

app = Flask(__name__)
CORS(app)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

@app.route('/', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "llama3-70b-8192", 
        "messages": [
            {"role": "system", "content": "You are a helpful assistant for the CM Reality website. Be friendly and concise."},
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.7,
        "max_tokens": 150
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        ai_reply = response.json()['choices'][0]['message']['content']
        return jsonify({"reply": ai_reply})
    except requests.exceptions.HTTPError as err:
        return jsonify({"reply": f"Groq API Error: {response.text}"}), 500
    except Exception as e:
        return jsonify({"reply": f"Other Error: {str(e)}"}), 500
