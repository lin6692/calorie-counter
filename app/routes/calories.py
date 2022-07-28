from flask import Blueprint, request, make_response, jsonify, abort
from app.models.user import User
from app import db
from app.routes.helper import get_calorie_from_food_API

calories_bp = Blueprint('calories_bp', __name__, url_prefix='/calories')


@calories_bp.route('', methods=['GET'])
def get_food_calories():
    request_body = request.get_json()
    try:
        search_term = request_body['search_term']
    except KeyError:
        abort(make_response(
            {'message': 'missing search_term', 'status_code': 400}), 400)

    food_cal = get_calorie_from_food_API(search_term)
    cal_per_gram, measures = food_cal['calorie_per_gram'], food_cal['measures']
    response_body = {}
    for measure in measures:
        label, weight = measure['label'], measure['weight'],
        key = f'1 {label}, {int(weight)}g'
        value = int(measure['weight'] * cal_per_gram)
        response_body[key] = value
    return jsonify(response_body), 200
