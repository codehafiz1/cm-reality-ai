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

@app.route('/chat', methods=['POST', 'OPTIONS'])
def chat():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200

    data = request.json
    user_message = data.get('message', '')
    image_data = data.get('image', None)

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    # Build the content array for the Vision model
    content = []
    if user_message:
        content.append({"type": "text", "text": user_message})
    else:
        content.append({"type": "text", "text": "What is in this image?"})

    if image_data:
        content.append({
            "type": "image_url",
            "image_url": {"url": image_data}
        })

    payload = {
        # Switched to Groq's Vision Model!
        "model": "llama-3.2-11b-vision-preview", 
        "messages": [
            {"role": "user", "content": content}
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
