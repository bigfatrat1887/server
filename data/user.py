from datetime import date
import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True, index=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    surname = sqlalchemy.Column(sqlalchemy.String)
    email = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True)
    gender = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    pic = sqlalchemy.Column(    # Не используется
        sqlalchemy.String,
        default='https://drive.google.com/file/d/1pLy_34cS-Fgi3VH8CSNjGNmmBikiEgbI/view?usp=sharing')
    hashed_password = sqlalchemy.Column(sqlalchemy.String)
    created_date = sqlalchemy.Column(sqlalchemy.Date, default=date.today())
    birthd = sqlalchemy.Column(sqlalchemy.Date,
                               default=date(2016, 7, 29))  # Не используется

    # Шифровка пароля
    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    # Проверка пароля?
    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    # Установка даты рождения по строке
    def set_b_time(self, string):
        self.birthd = date.strptime(string, "%d-%m-%Y")

    # Установка пола (спасибо питон)
    def set_gender(self, string):
        choice = {'True': True, 'False': False}
        self.gender = choice[string]

# DONE
