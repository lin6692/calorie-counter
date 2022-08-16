from flask import Blueprint, request, make_response, jsonify, abort
from app.models.user import User
from app import db
from app.routes.helper import get_calorie_from_food_API

calories_bp = Blueprint('calories_bp', __name__, url_prefix='/calories')


@calories_bp.route('', methods=['GET'])
def get_food_calories():
    search_term = request.args.get('search_term')
    food_cal = get_calorie_from_food_API(search_term)
    cal_per_gram, measures = food_cal['calorie_per_gram'], food_cal['measures']
    name = food_cal['name']
    response_body = {'name': name, 'whole': [],
                     'ounce': [], 'serving': [], 'slice': []}
    for measure in measures:
        label, weight = measure['label'].lower(), int(measure['weight'])
        calories = int(weight * cal_per_gram)
        if label in response_body.keys():
            response_body[label] = [weight, calories]

    return jsonify(response_body), 200
