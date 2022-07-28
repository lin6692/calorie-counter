from flask import Blueprint, request, make_response, jsonify, abort
from app.models.user import User
from app import db

users_bp = Blueprint('users_bp', __name__, url_prefix='/users')


@users_bp.route('', methods=['GET'])
def get_all_users():
    users = User.objects()
    return jsonify(users), 201


@users_bp.route('/<user_id>', methods=['PATCH'])
def update_one_user(user_id):
    request_body = request.get_json()
    user = User.get_user(user_id)
    if not user:
        abort(make_response(
            {'message': 'user not found', 'status_code': 404}, 404))
    user.update(**request_body)
    return jsonify({'message': f'User {user_id} has been updated', 'status_code': 200}), 200


@users_bp.route('/<user_id>', methods=['DELETE'])
def delete_one_user(user_id):
    user = User.get_user(user_id)
    if not user:
        abort(make_response(
            {'message': 'user not found', 'status_code': 404}, 404))
    user.delete()
    return jsonify({'message': f'User {user_id} has been deleted', 'status_code': 200}), 200

# @users_bp.route('', methods=['POST'])
# def create_user():
#     request_body = request.get_json()
#     new_user_id = User.objects().order_by(
#         '-user_id')[0]['user_id'] + 1        # <--- update this line

#     try:
#         user = User(user_id=new_user_id, **request_body).save()
#     except mongoengine.errors.ValidationError as e:
#         abort(make_response(
#             {'message': 'missing info in request body', 'details': e.message, 'status_code': 400}, 400))
#     except mongoengine.errors.NotUniqueError:
#         abort(make_response(
#             {'message': 'User name is taken', 'status_code': 400}, 400))

#     return jsonify(user), 201


# @users_bp.route('/<user_id>', methods=['GET'])
# def get_one_user(user_id):
#     user_id = ObjectId(user_id)
#     user = User.get_user(user_id)
#     if not user:
#         abort(make_response(
#             {'message': 'user not found', 'status_code': 404}, 404))
#     return jsonify(user), 200
