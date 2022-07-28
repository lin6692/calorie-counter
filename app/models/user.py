from app import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(email):
    return User.objects(email=email).first()


class User(db.Document, UserMixin):
    user_id = db.StringField(required=True, unique=True)
    user_name = db.StringField(required=True)
    email = db.EmailField(required=True, unique=True)
    gender = db.StringField()
    age = db.IntField()
    height = db.IntField()
    weight = db.IntField()
    daily_calorie_intake = db.IntField(required=True)

    @staticmethod
    def get_user(user_id):
        user_id = str(user_id)
        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return None
        return user

    def get_id(self):
        return self.email
