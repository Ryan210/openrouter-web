from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv
import sys

# 打印当前工作目录
print(f"Current working directory: {os.getcwd()}")

# 打印 .env 文件的绝对路径
env_path = os.path.join(os.getcwd(), '.env')
print(f".env file path: {env_path}")
print(f".env file exists: {os.path.exists(env_path)}")

# 尝试直接读取 .env 文件
try:
    with open(env_path, 'r') as f:
        print(f".env file content: {f.read()}")
except Exception as e:
    print(f"Error reading .env file: {e}")

# 加载环境变量
load_dotenv(env_path)

app = Flask(__name__)
CORS(app)

OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
print(f"Loaded API key: {OPENROUTER_API_KEY}")

if not OPENROUTER_API_KEY or OPENROUTER_API_KEY == 'your_api_key_here':
    print("警告: API 密钥未设置！请在 .env 文件中设置 OPENROUTER_API_KEY")

CHAT_API_URL = "https://openrouter.ai/api/v1/chat/completions"
IMAGE_API_URL = "https://openrouter.ai/api/v1/images/generations"

@app.route('/')
def index():
    if not OPENROUTER_API_KEY or OPENROUTER_API_KEY == 'your_api_key_here':
        return render_template('index.html', api_key_error=True)
    return render_template('index.html', api_key_error=False)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        if not OPENROUTER_API_KEY or OPENROUTER_API_KEY == 'your_api_key_here':
            return jsonify({
                "error": "API Error",
                "message": "API 密钥未设置！请在 .env 文件中设置 OPENROUTER_API_KEY"
            }), 401
        
        data = request.json
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": request.headers.get('Host', 'localhost:5000'),
            "X-Title": "Open Router Web Interface"
        }
        
        payload = {
            "model": data.get('model', 'openai/gpt-3.5-turbo'),
            "messages": data['messages'],
            "temperature": 0.7,
            "max_tokens": 1000
        }
        
        response = requests.post(CHAT_API_URL, headers=headers, json=payload)
        
        if response.status_code != 200:
            return jsonify({
                "error": f"API Error: {response.status_code}",
                "message": response.text
            }), response.status_code
            
        return response.json()
    except Exception as e:
        return jsonify({
            "error": "Server Error",
            "message": str(e)
        }), 500

@app.route('/generate-image', methods=['POST'])
def generate_image():
    try:
        if not OPENROUTER_API_KEY or OPENROUTER_API_KEY == 'your_api_key_here':
            return jsonify({
                "error": "API Error",
                "message": "API 密钥未设置！请在 .env 文件中设置 OPENROUTER_API_KEY"
            }), 401
        
        data = request.json
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": request.headers.get('Host', 'localhost:5000'),
            "X-Title": "Open Router Web Interface"
        }
        
        payload = {
            "model": data.get('model', 'stabilityai/stable-diffusion-xl'),
            "prompt": data['prompt'],
            "n": 1,
            "size": "1024x1024"
        }
        
        response = requests.post(IMAGE_API_URL, headers=headers, json=payload)
        
        if response.status_code != 200:
            return jsonify({
                "error": f"API Error: {response.status_code}",
                "message": response.text
            }), response.status_code
            
        return response.json()
    except Exception as e:
        return jsonify({
            "error": "Server Error",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
