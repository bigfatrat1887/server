import datetime
import os

from flask import Flask, render_template, redirect, make_response, jsonify
from requests import post, delete, put, get
from data.news import News
from data.user import User
from forms.news import PostForm, PutForm
from forms.user import RegisterForm, LoginForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from data import db_session, user_api, news_api

# Инициализация приложения
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(
    days=365
)
# Подключение утилиты для входа
login_manager = LoginManager()
login_manager.init_app(app)
# Подключение БД к Серверу и прилагающимся
db_session.global_init("db/web.sqlite")
# Подключение великого и ужасного API для Users let`s say
app.register_blueprint(user_api.blueprint)
app.register_blueprint(news_api.blueprint)
   

# Для казусов
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


# Вход пользователя
@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


# Пустой запрос
@app.route("/")
def index():
    db_sess = db_session.create_session()
    news = db_sess.query(News)
    return render_template("news.html", news=news)


# Страница входа
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', form=form)


# Страница выхода
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


# Регистрация
@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html',
                                   form=form,
                                   message="Такой пользователь уже есть")

        post('https://betanet.herokuapp.com/api/users', json={'name': form.name.data,
                                                      'surname': form.surname.data,
                                                      'email': form.email.data,
                                                      'gender': form.gender.data,
                                                      'hashed_password': form.password.data})
        return redirect('/')
    return render_template('register.html', form=form)


# Добавление новости
@app.route('/news_post',  methods=['GET', 'POST'])
@login_required
def add_news():
    form = PostForm()
    if form.validate_on_submit():
        post('https://betanet.herokuapp.com/api/news', json={
            'text': form.text.data.capitalize(),
            'user_id': current_user.id

        })
        return redirect('/')
    return render_template('news_post.html',
                           form=form)


# Изменение новости
@app.route('/news_edit/<int:news_id>', methods=['GET', 'POST', 'PUT'])
@login_required
def edit_news(news_id):
    form = PutForm()
    news = get(f'https://betanet.herokuapp.com/api/news/{news_id}').json()['news']
    if form.validate_on_submit():
        put(f'https://betanet.herokuapp.com/api/news/{news_id}', json={
            'text': form.text.data.capitalize()
        }).json()
        return redirect('/')
    return render_template('news_put.html', text=news['text'] + ' ->', form=form)


# Удаление новости
@app.route('/news_delete/<int:news_id>', methods=['GET', 'POST', 'DELETE'])
@login_required
def news_delete(news_id):
    delete(f'https://betanet.herokuapp.com/api/news/{news_id}').json()
    return redirect('/')


# Обработчик лайка
@app.route('/news_like/<int:news_id>', methods=['GET', 'PUT', 'POST'])
@login_required
def like_news(news_id):
    news = get(f'https://betanet.herokuapp.com/api/news/{news_id}').json()['news']
    uid = str(current_user.id)
    if uid not in news['list_like'].split():
        edited = news['list_like'].split()
        edited.append(uid + '')
        edited = ' '.join(edited)
        put(f'https://betanet.herokuapp.com/api/news/{news_id}', json={'like': news['like'] + 1,
                                                             'list_like': edited})
    else:
        edited = news['list_like'].split()
        del edited[edited.index(uid)]
        edited = ' '.join(edited)
        put(f'https://betanet.herokuapp.com/api/news/{news_id}', json={'like': news['like'] - 1,
                                                             'list_like': edited})
    return redirect('/')


# Обработчик дизлайка
@app.route('/news_dislike/<int:news_id>', methods=['GET', 'PUT', 'POST'])
@login_required
def dislike_news(news_id):
    news = get(f'https://betanet.herokuapp.com/api/news/{news_id}').json()['news']
    uid = str(current_user.id)
    if uid not in news['list_dislike'].split():
        edited = news['list_dislike'].split()
        edited.append(uid)
        edited = ' '.join(edited)
        put(f'https://betanet.herokuapp.com/api/news/{news_id}', json={'dislike': news['dislike'] + 1,
                                                             'list_dislike': edited})
    else:
        edited = news['list_dislike'].split()
        del edited[edited.index(uid)]
        edited = ' '.join(edited)
        put(f'https://betanet.herokuapp.com/api/news/{news_id}', json={'dislike': news['dislike'] - 1,
                                                             'list_dislike': edited})
    return redirect('/')


if __name__ == '__main__':
    # ПОiХАЛИ
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
