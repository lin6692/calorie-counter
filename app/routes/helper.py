from flask import Blueprint, request, make_response, jsonify, abort
from app.models.user import User
from app import db
import mongoengine


def valid_user(user_id):
    try:
        user = User.objects.get(user_id=user_id)
    except User.DoesNotExist:
        abort(make_response(
            {'message': 'User_id does not exist', 'status_code': 404}, 404))
    return user
