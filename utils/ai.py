import requests
from flask import request, jsonify

URL = 'http://localhost:11434/api/generate'


def ask_ollama():
    data = request.get_json()
    prompt = data.get('prompt')

    if not prompt:
        return jsonify({'success': False, 'message': 'Prompt is required'}), 400

    payload = {
        'model': 'llama3.2',
        'stream': False,
        'prompt': prompt
    }
    try:
        response = requests.post(URL, json=payload)
        response_data = response.json()
        if response_data["response"]:
            return jsonify({'success': True, 'data': response_data["response"]}), response.status_code
        else:
            return jsonify({'success': False, 'message': "No data received from request"}), 500
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
