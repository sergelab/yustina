# coding: utf-8
from __future__ import absolute_import

from flask_login import UserMixin
from yustina.init import db
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import check_password_hash, generate_password_hash


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), unique=True, nullable=False)
    pw_hash = db.Column(db.String(68), nullable=True)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)

    @classmethod
    def get_by_username(cls, username):
        """
        Получение объекта пользователя по логину.
        :param username: Имя пользователя
        :return: User
        """
        return cls.query.filter(
            cls.username.__eq__(username)
        ).first()

    @hybrid_property
    def password(self):
        return self.pw_hash

    @password.setter
    def password(self, password):
        if password:
            self.pw_hash = generate_password_hash(password)
