from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Vercel automatically routes /api to this file. We just need the '/' route.
@app.route('/', methods=['POST', 'OPTIONS'])
def chat():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200

    user_message = request.json.get('message')
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "llama-3.3-70b-versatile", 
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
