from app import db
from flask import make_response, abort


class User(db.Document):
    user_id = db.IntField(required=True, unique=True)
    user_name = db.StringField(required=True, unique=True)
    email = db.StringField(required=True, unique=True)
    gender = db.StringField()
    age = db.IntField()
    height = db.IntField()
    weight = db.IntField()
    daily_calorie_intake = db.IntField(required=True)
    # login_id = db.StringField(required=True, unique=True)

    @staticmethod
    def get_user(user_id):
        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            abort(make_response(
                {'message': f'User Not Found', 'status_code': 404}), 404)
        return user
