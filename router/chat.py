from dotenv import load_dotenv
from flask import Blueprint, request

from utils.db import Database
from utils.queries import SQLQuery

load_dotenv()
db = Database()

chat_bp = Blueprint('chat', __name__)


# @chat_bp.route('/users/<int:user_id>', methods=['GET'])
# async def get_user_by_id(user_id):
#     query = "SELECT * FROM [user] WHERE id = ?"
#     result = await sql_fetch_query(db, query, (user_id))
#     if result.json['data']:
#         return jsonify(result.json['data'][0])
#     return jsonify({'success': False, 'message': 'User not found'}), 404
#
#
# @chat_bp.route('/messages', methods=['GET'])
# async def get_messages():
#     query = "SELECT * FROM message WHERE isDeleted = 0"
#     query_object = SQLQuery(query, ())
#     return await sql_fetch_query(db, query_object)


@chat_bp.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()

    message = data.get('message')
    sender_id = data.get('senderId')
    receiver_id = data.get('receiverId')
    query_object = SQLQuery(
        "INSERT INTO message (message, senderId, receiverId) OUTPUT INSERTED.* VALUES (?, ?, ?)",
        (message, sender_id, receiver_id)
    )
    return db.fetch_query(query_object)

# @chat_bp.route('/messages', methods=['PUT'])
# def edit_message():
#     data = request.get_json()
#     query = SQLQuery(
#         "UPDATE message SET message = ?, editedAt = ? OUTPUT INSERTED.* WHERE id = ?",
#         (data['message'], datetime.utcnow(), data['id'])
#     )
#     result = sql_execute_query(db, query)
#     if result.json['success']:
#         emit('receive_message', result.json['data'][0], broadcast=True)
#     return result
#
#
# @chat_bp.route('/messages', methods=['DELETE'])
# def delete_message():
#     data = request.get_json()
#     query = SQLQuery(
#         "UPDATE message SET isDeleted = 1, deletedAt = ? OUTPUT INSERTED.* WHERE id = ?",
#         (datetime.utcnow(), data['id'])
#     )
#     result = sql_execute_query(db, query)
#     if result.json['success']:
#         emit('receive_message', result.json['data'][0], broadcast=True)
#     return result
