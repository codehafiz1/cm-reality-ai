from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Changed to Groq!
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    
    # Groq's API URL
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        # Using Llama 3 on Groq (super fast!)
        "model": "llama3-8b-8192", 
        "messages": [
            {"role": "system", "content": "You are a helpful assistant for the CM Reality website. Be friendly and concise."},
            {"role": "user", "content": user_message}
        ]
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        ai_reply = response.json()['choices'][0]['message']['content']
        return jsonify({"reply": ai_reply})
    except Exception as e:
        # We will keep this so if there's an error, it tells us exactly what it is
        return jsonify({"reply": f"Backend Error: {str(e)}"}), 500

# Update for Vercel
