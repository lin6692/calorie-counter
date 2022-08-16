from flask import Blueprint, request, make_response, jsonify, abort
from app.models.user import User
from app import db
import mongoengine
import requests
import os


def get_calorie_from_food_API(search_term):
    URL = 'https://api.edamam.com/api/food-database/v2/parser'
    app_id = os.environ.get("FOOD_API_ID")
    app_key = os.environ.get("FOOD_API_KEY")
    params = {
        'app_id': app_id,
        'app_key': app_key,
        'ingr': search_term
    }

    response = requests.get(URL, params=params)
    food_data = response.json()
    calorie_data = food_data['hints'][0]
    return {'name': calorie_data['food']["label"],
            'calorie_per_gram': calorie_data['food']['nutrients']['ENERC_KCAL']/100,
            'measures': calorie_data['measures']}
