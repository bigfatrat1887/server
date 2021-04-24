import flask
from flask import jsonify
from . import db_session
from .user import User
from flask_restful import reqparse, abort, Resource, Api
# Создадим чертеж API пользователей
blueprint = flask.Blueprint(
    'user_api',
    __name__,
    template_folder='templates'
)
# Зарегистрируем приложение как API
api = Api(blueprint)


# Создадим проверку на отсутствие пользователя
def abort_nouser(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")


# Парсер для PUT запросов
put_parser = reqparse.RequestParser()
put_parser.add_argument('name', type=str)
put_parser.add_argument('surname', type=str)
put_parser.add_argument('email', type=str)
put_parser.add_argument('hashed_password', type=str)
put_parser.add_argument('gender', type=str)


# Класс запросов для единичного пользователя
class UserResource(Resource):
    # Возврат пользователя
    def get(self, user_id):
        abort_nouser(user_id)
        db_sess = db_session.create_session()
        users = db_sess.query(User).get(user_id)
        return jsonify(
            {
                'users': users.to_dict(only=('id', 'name', 'surname', 'gender', 'email',
                                             'birthd', 'created_date'))
            }
        )

    # Удаление пользователя
    def delete(self, user_id):
        abort_nouser(user_id)
        db_sess = db_session.create_session()
        user = db_sess.query(User).get(user_id)
        db_sess.delete(user)
        db_sess.commit()
        return jsonify({'Success': 'OK'})

    # Редактирование пользователя
    def put(self, user_id):
        abort_nouser(user_id)
        args = put_parser.parse_args()
        # Проверка None
        if all(args[key] is None for key in args):
            return jsonify({'Error': 'Empty request'})
        else:
            db_sess = db_session.create_session()
            user = db_sess.query(User).get(user_id)
            # Проверки для запроса редактирования
            # Парсер заполняет значения без required как None, нужна такая система проверки
            if args['name']:
                user.name = args['name']
            if args['surname']:
                user.surname = args['surname']
            if args['email']:
                user.email = args['email']
            if args['hashed_password']:
                user.set_password(args['hashed_password'])
            if args['gender']:
                user.set_gender(args['gender'])
            db_sess.commit()
            return jsonify({'Success': 'OK'})


# Парсер для POST запросов
post_parser = reqparse.RequestParser()
post_parser.add_argument('name', required=True, type=str)
post_parser.add_argument('surname', required=True, type=str)
post_parser.add_argument('email', required=True, type=str)
post_parser.add_argument('hashed_password', required=True, type=str)
post_parser.add_argument('gender', required=True, type=str)


# Класс запросов с индексом
class UserListResource(Resource):
    # Возврат группы
    def get(self):
        db_sess = db_session.create_session()
        users = db_sess.query(User).all()
        return jsonify(
            {
                'users':
                    [item.to_dict(only=('id', 'name', 'surname',
                                        'gender', 'email', 'birthd', 'created_date')) for item in users]
            }
        )

    # Cоздание нового пользователя
    def post(self):
        args = post_parser.parse_args()
        db_sess = db_session.create_session()
        # Принимаем аргументы в парсере
        user = User(
            name=args['name'],
            surname=args['surname'],
            email=args['email'],
        )
        # Передаем пароль в хеширующую функцию
        user.set_password(args['hashed_password'])
        user.set_gender(args['gender'])
        db_sess.add(user)
        db_sess.commit()
        return jsonify({'Success': 'OK'})


# Заключительная регистрация в API единичных запросов
api.add_resource(UserListResource, '/api/users')
# Заключительная регистрация в API запросов с индексом
api.add_resource(UserResource, '/api/users/<int:user_id>')