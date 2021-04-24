from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import SubmitField
from wtforms.validators import DataRequired


# Добавление новости
class PostForm(FlaskForm):
    text = StringField('Содержание новости', validators=[DataRequired()])
    submit_add = SubmitField('Добавить')


# Редактирование новости
class PutForm(FlaskForm):
    text = StringField('Содержание новости', validators=[DataRequired()])
    submit_edit = SubmitField('Изменить')

