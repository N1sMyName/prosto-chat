from flask import Flask, request
from flask_cors import CORS
from router.chat import chat_bp
from utils.ai import ask_ollama
from utils.db import Database
from utils.queries import insert_into_text_class_query

app = Flask(__name__)
CORS(app)
# socketio = SocketIO(app, cors_allowed_origins="*")
db = Database()

app.register_blueprint(chat_bp, url_prefix='/chat')


@app.route('/create_entry', methods=['POST'])
async def create_entry():
    data = request.get_json()
    label = data.get('label')
    text = data.get('text')
    query_object = insert_into_text_class_query((label, text))
    return await db.execute_query(query_object)


@app.route('/ollama', methods=['POST'])
def ollama():
    return ask_ollama()


# @socketio.on('connect')
# def handle_connect():
#     print('Client connected')
#
#
# @socketio.on('disconnect')
# def handle_disconnect():
#     print('Client disconnected')
#
#
# @socketio.on('send_message')
# def handle_send_message(data):
#     # Broadcast the message to all connected clients
#     emit('receive_message', data, broadcast=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
