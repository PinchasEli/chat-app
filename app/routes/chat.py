
from flask import request, Blueprint
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import db

from app.middlewares import ResponseHandler

from app.models import User, Chat, Message

chat_bp = Blueprint('chat', __name__, url_prefix='/chat')

@chat_bp.route('', methods=['GET'])
@cross_origin()
@jwt_required()
def get_chat_list():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    chat_list = Chat.query.filter_by(user_id=user.id, active=True).all()
    chat_list_data = [{
        'id': chat.id,
        'createdAt': chat.created_at
    } for chat in chat_list]

    return ResponseHandler.success(chat_list_data)


@chat_bp.route('/new', methods=['POST'])
@jwt_required()
@cross_origin()
def create_chat():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if not user:
        return ResponseHandler.error({'msg': 'User not found'}, 404)

    chat = Chat(user_id=user.id)
    db.session.add(chat)
    db.session.commit()
    return ResponseHandler.success({
        'id': chat.id,
        'createdAt': chat.created_at
    })


@chat_bp.route('/<int:chat_id>/messages', methods=['GET'])
@jwt_required()
@cross_origin()
def get_chat_messages(chat_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if not user:
        return ResponseHandler.error({'msg': 'User not found'}, 404)

    chat = Chat.query.filter_by(id=chat_id).first()
    if not chat:
        return ResponseHandler.error({'msg': 'Chat not found'}, 404)

    message_list = Message.query.filter_by(chat_id=chat.id).order_by(Message.created_at).all()
    message_list_data = [{
        'id': message.id,
        'chatId': message.chat_id,
        'question': message.question,
        'answer': message.answer,
        'createdAt': message.created_at
    } for message in message_list]

    return ResponseHandler.success(message_list_data)


@chat_bp.route('/message', methods=['POST'])
@jwt_required()
@cross_origin()
def create_message():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if not user:
        return ResponseHandler.error({'msg': 'User not found'}, 404)

    data = request.json
    if not data or not data.get('chatId') or not data.get('question'):
        return ResponseHandler.error({'msg': 'Content field is required'}, 400)

    chat = Chat.query.filter_by(id=data.get('chatId')).first()
    if not chat:
        return ResponseHandler.error({'msg': 'Chat not found'}, 404)

    message = Message(question=data['question'], answer=data['question'][::-1], chat_id=chat.id)
    db.session.add(message)
    db.session.commit()
    return ResponseHandler.success({
        'id': message.id,
        'chatId': message.chat_id,
        'question': message.question,
        'answer': message.answer,
        'createdAt': message.created_at
    })
