from datetime import date
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


# класс постов/новостей
class News(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'news'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    created_date = sqlalchemy.Column(sqlalchemy.Date, default=date.today())
    like = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    dislike = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    list_like = sqlalchemy.Column(sqlalchemy.String, default='0')
    list_dislike = sqlalchemy.Column(sqlalchemy.String, default='0')
    text = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    photo = sqlalchemy.Column(sqlalchemy.String,
                              default='https://demotivation.ru/wp-content/uploads/2020/03/Baking_Blueberries_440238.jpg')
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), nullable=False)
    user = orm.relation('User')
