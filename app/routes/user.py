from datetime import timedelta

from flask import request, Blueprint
from flask_jwt_extended import create_access_token, jwt_required
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.middlewares import ResponseHandler

from app.models import User

user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route('', methods=['GET'])
@cross_origin()
@jwt_required()
def get_user():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return ResponseHandler.error({'msg': 'User not found'}, 404)

    user_data = {
        'id': user.id,
        'username': user.username
    }

    return ResponseHandler.success(user_data)


@user_bp.route('/login', methods=['POST'])
@cross_origin()
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    user = User.query.filter_by(username=username, password=password).first()

    if user:
        access_token = create_access_token(identity=user.id, expires_delta=timedelta(minutes=60))
        return ResponseHandler.success({
                'access_token': access_token,
                'user': {
                    'id': user.id,
                    'username': user.username
                }
            })

    return ResponseHandler.error({'msg': 'Invalid username or password'}, 401)
