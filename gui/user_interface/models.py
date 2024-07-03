from datetime import datetime
from datetime import timedelta

from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer as Serializer
from sqlalchemy import asc
from werkzeug.security import check_password_hash, generate_password_hash

from .config import Config
from ..user_interface import db


class TaskMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.DateTime, default=datetime.now)
    task_id = db.Column(db.String)
    message = db.Column(db.String)
    signal = db.Column(db.String)
    user_id = db.Column(db.String)

    @staticmethod
    def newest(_time):
        return TaskMessage.query.order_by(asc('date')).filter(
            TaskMessage.date.between((datetime.now() - timedelta(0, _time)), datetime.now())).all()

    @staticmethod
    def all():
        return TaskMessage.query.all()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String)
    primary_user = db.Column(db.Boolean)

    def get_reset_token(self, expires_sec=300):
        s = Serializer(Config.SECRET_KEY, expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get_by_username(username):
        return User.query.filter_by(username=username).first()

    @staticmethod
    def verify_token(token):
        s = Serializer(Config.SECRET_KEY)
        try:
            user_id = s.loads(token)['user_id']
        except:
            return
        else:
            return User.query.get(user_id)

    def __repr__(self):
        return "<User '{}'>".format(self.username)
