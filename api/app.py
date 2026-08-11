from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
from dotenv import load_dotenv

# Load environment variables (Vercel will provide these automatically)
load_dotenv()

app = Flask(__name__)
CORS(app)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "google/gemma-7b-it:free", 
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
        print(f"Error: {e}")
        return jsonify({"reply": "Sorry, I am having trouble connecting to the AI right now."}), 500

# Removed the app.run() part because Vercel handles the server automatically!