from logging.config import valid_ident
from flask import Blueprint, request, make_response, jsonify, abort
from app.models.user import User
from app import db
import mongoengine
from app.routes.helper import valid_user

calories_bp = Blueprint('calories_bp', __name__, url_prefix='/calories')


@calories_bp.route('/<user_id>', methods=['GET'])
def get_calories_by_user(user_id):
    user = valid_user(user_id)
    daily_calorie_intake = user.daily_calorie_intake

    if daily_calorie_intake is None:
        gender = user.gender
        weight = user.weight
        height = user.height
        age = user.age

        if not (gender and weight and height and age):
            abort(make_response(
                {'message': 'Please complete the profile to get calculated daily calorie\
                or manually enter the calorie goal', 'status_code': 404}, 404))

        # calculate daily calorie intake
        if gender == 'F':
            daily_calorie_intake = 655.1 + 9.563*weight + 1.850*height - 4.676*age
        elif gender == 'M':
            daily_calorie_intake = 66.47 + 13.75*weight + 5.003*height - 6.755*age

        User.objects(user_id=user_id).update_one(
            daily_calorie_intake=daily_calorie_intake)

    return jsonify(daily_calorie_intake), 200


@calories_bp.route('/<user_id>', methods=['PATCH'])
def update_calories_by_user(user_id):
    valid_user(user_id)
    request_body = request.get_json()
    try:
        daily_calorie_intake = request_body['daily_calorie_intake']
    except KeyError:
        abort(make_response(
            {'message': 'Missing daily_calorie_intake in request body', 'status_code': 400}, 400))

    User.objects(user_id=user_id).update_one(
        daily_calorie_intake=daily_calorie_intake)

    return jsonify({'message': f'User {user_id} daily_calorie_intake has been updated to {daily_calorie_intake}', 'status_code': 200}), 200


@calories_bp.route('/<search_param>', methods=['GET'])
def get_food_calories(serach_param):
    pass
