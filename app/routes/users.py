from flask import Blueprint, request, make_response, jsonify, abort
from app.models.user import User
from app import db
import mongoengine

users_bp = Blueprint('users_bp', __name__, url_prefix='/users')


@users_bp.route('', methods=['POST'])
def create_user():
    request_body = request.get_json()

    try:
        user = User(**request_body).save()
    except mongoengine.errors.ValidationError as e:
        abort(make_response(
            {'message': 'missing info in request body', 'details': e.message, 'status_code': 400}, 400))
    except mongoengine.errors.NotUniqueError:
        abort(make_response(
            {'message': 'User name is taken', 'status_code': 400}, 400))

    return make_response(
        jsonify(user), 201
    )
