from dotenv import load_dotenv
from flask import Blueprint, request, jsonify

from utils.db import Database
from utils.queries import SQLQuery

load_dotenv()
db = Database()

chat_bp = Blueprint('chat', __name__)

@chat_bp.before_request
def handle_options_request():
    if request.method == 'OPTIONS':
        return jsonify({'success': True}), 200


@chat_bp.route('/users/<int:user_id>', methods=['GET'])
async def get_user_by_id(user_id):
    query = f"SELECT * FROM [user] WHERE id = {user_id}"
    query_object = SQLQuery(query, ())
    return await db.fetch_query(query_object)


#
#
@chat_bp.route('/messages', methods=['GET'])
async def get_messages():
    query = "SELECT * FROM message WHERE isDeleted = 0"
    query_object = SQLQuery(query, ())
    return await db.fetch_query(query_object)


@chat_bp.route('/messages', methods=['POST'])
async def create_message():
    data = request.get_json()

    message = data.get('message')
    sender_id = data.get('senderId')
    receiver_id = data.get('receiverId')
    query_object = SQLQuery(
        "INSERT INTO message (message, senderId, receiverId) OUTPUT INSERTED.* VALUES (?, ?, ?)",
        (message, sender_id, receiver_id)
    )
    return await db.fetch_query(query_object)


@chat_bp.route('/messages', methods=['PUT'])
async def edit_message():
    data = request.get_json()
    query_object = SQLQuery(
        "UPDATE message SET message = ? OUTPUT INSERTED.* WHERE id = ?",
        (data['message'], data['id'])
    )
    print('emit to websocket here')
    return await db.fetch_query(query_object)
    # emit('receive_message', result.json['data'][0], broadcast=True)


@chat_bp.route('/messages/<int:message_id>', methods=['DELETE'])
async def delete_message(message_id):
    query = SQLQuery(
        f"UPDATE message SET isDeleted = 1 OUTPUT INSERTED.* WHERE id = {message_id}",
        (),
        "Message was successfully deleted"
    )
    # emit('receive_message', result.json['data'][0], broadcast=True)
    return await db.execute_query(query)
