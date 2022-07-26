from app import db


class User(db.Document):
    user_name = db.StringField(required=True, unique=True)
    email = db.StringField(required=True)
    gender = db.StringField()
    age = db.IntField()
    height = db.IntField()
    weight = db.IntField()
    daily_calorie_intake = db.IntField()
