import os
import json
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

HF_API_TOKEN = os.environ.get("HF_API_TOKEN")
HF_MODEL = "tiiuae/gemini-2-2b"

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    
    # Build prompt
    prompt = """You are CooLLaMA, a fun and helpful chatbot for a website.
Answer clearly and cheerfully.

User: {user_message}
CooLLaMA:"""
    
    headers = {
        "Authorization": f"Bearer {HF_API_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "inputs": prompt
    }
    
    response = requests.post(
        f"https://api-inference.huggingface.co/models/{HF_MODEL}",
        headers=headers,
        json=payload
    )
    
    result = response.json()
    text = result[0].get("generated_text", "Sorry, I couldn't respond.")
    return jsonify({"response": text})

if __name__ == "__main__":
    app.run(debug=True)
