from flask import Blueprint, request, make_response, jsonify, abort
from app.models.user import User
from app import db
import mongoengine
from app.routes.helper import valid_user

users_bp = Blueprint('users_bp', __name__, url_prefix='/users')


@users_bp.route('', methods=['POST'])
def create_user():
    request_body = request.get_json()
    new_user_id = User.objects().order_by('-user_id')[0]['user_id'] + 1

    try:
        user = User(user_id=new_user_id, **request_body).save()
    except mongoengine.errors.ValidationError as e:
        abort(make_response(
            {'message': 'missing info in request body', 'details': e.message, 'status_code': 400}, 400))
    except mongoengine.errors.NotUniqueError:
        abort(make_response(
            {'message': 'User name is taken', 'status_code': 400}, 400))

    return jsonify(user), 201


@users_bp.route('', methods=['GET'])
def get_all_users():
    users = User.objects()
    return jsonify(users), 201


@users_bp.route('/<user_id>', methods=['GET'])
def get_one_user(user_id):
    user = valid_user(user_id)
    return jsonify(user), 200


@users_bp.route('/<user_id>', methods=['PATCH'])
def update_one_user(user_id):
    request_body = request.get_json()
    if "user_id" in request_body:
        abort(make_response(
            {'message': 'user_id can\'t be udpated', 'status_code': 400}, 400))

    user = valid_user(user_id)
    user.update(**request_body)
    return jsonify({'message': f'User {user_id} has been updated', 'status_code': 200}), 200


@users_bp.route('/<user_id>', methods=['DELETE'])
def delete_one_user(user_id):
    user = valid_user(user_id)
    user.delete()
    return jsonify({'message': f'User {user_id} has been deleted', 'status_code': 200}), 200
