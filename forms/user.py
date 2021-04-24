from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, \
    SubmitField, BooleanField, \
    SelectField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


# Форма Регистрации
class RegisterForm(FlaskForm):
    name = StringField('Имя пользователя', validators=[DataRequired()])
    surname = StringField('Фамилия пользователя', validators=[DataRequired()])
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    gender = SelectField('Пол', choices=[(False, 'Выберите пол:'), ('True', 'Мужской'),
                                         ('False', 'Женский')], validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')


# Форма Входа
class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

