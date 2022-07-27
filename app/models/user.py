from app import db


class User(db.Document):
    user_id = db.IntField(required=True, unique=True)
    user_name = db.StringField(required=True, unique=True)
    email = db.StringField(required=True, unique=True)
    gender = db.StringField()
    age = db.IntField()
    height = db.IntField()
    weight = db.IntField()
    daily_calorie_intake = db.IntField()
