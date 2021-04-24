import flask
from flask import jsonify
from flask_restful import reqparse, abort, Api, Resource
from data import db_session
from data.news import News

blueprint = flask.Blueprint(
    'news_api',
    __name__,
    template_folder='templates'
)
api = Api(blueprint)
# Парсинг для запросов на изменение
put_parser = reqparse.RequestParser()
put_parser.add_argument('text', type=str)
put_parser.add_argument('photo', type=str)
put_parser.add_argument('like', type=int)
put_parser.add_argument('dislike', type=int)
put_parser.add_argument('list_like', type=str)
put_parser.add_argument('list_dislike', type=str)


# Проверка на наличие новости по ID
def abort_if_news_not_found(news_id):
    db_session.global_init("db/blogs.sqlite")
    session = db_session.create_session()
    news = session.query(News).get(news_id)
    if not news:
        abort(404, message=f"News {news_id} not found")


# Класс для запросам по ID
class NewsResource(Resource):
    # Получение одной новости
    def get(self, news_id):
        abort_if_news_not_found(news_id)
        session = db_session.create_session()
        news = session.query(News).get(news_id)
        return jsonify(
            {
                'news': news.to_dict(only=('id', 'user_id', 'text', 'like',
                                           'dislike', 'list_like',
                                           'list_dislike', 'created_date', 'user_id'))
            }
        )

    # Удаление одной новости
    def delete(self, news_id):
        abort_if_news_not_found(news_id)
        session = db_session.create_session()
        news = session.query(News).get(news_id)
        session.delete(news)
        session.commit()
        return jsonify({'success': 'OK'})

    # Изменение одной новости
    def put(self, news_id):
        abort_if_news_not_found(news_id)
        args = put_parser.parse_args()
        if all(args[key] is None for key in args):
            return jsonify({'Error': 'Empty request'})
        else:
            db_sess = db_session.create_session()
            news = db_sess.query(News).get(news_id)
            # Проверки для запроса редактирования
            if args['text']:
                news.text = args['text']
            if args['photo']:
                news.photo = args['photo']
            if 'like' in args and args['like'] is not None:
                news.like = args['like']
            if 'dislike' in args and args['dislike'] is not None:
                news.dislike = args['dislike']
            if args['list_like']:
                news.list_like = args['list_like']
            if args['list_dislike']:
                news.list_dislike = args['list_dislike']
            db_sess.commit()
            return jsonify({'Success': 'OK'})


# Парсим аргументы для создания новой новости
post_parser = reqparse.RequestParser()
post_parser.add_argument('user_id', required=True, type=int)
post_parser.add_argument('text', required=True, type=str)


# Для общих запросов, создания новости
class NewsListResource(Resource):
    # Получение всех новостей
    def get(self):
        session = db_session.create_session()
        news = session.query(News).all()
        return jsonify(
            {
                'news': [item.to_dict(only=('id', 'user_id', 'text', 'like',
                                            'dislike', 'list_like',
                                            'list_dislike', 'created_date', 'user_id')) for item in news]
            }
        )

    # Слздание новой новости
    def post(self):
        args = post_parser.parse_args()
        session = db_session.create_session()
        news = News(
            text=args['text'],
            user_id=args['user_id']
        )
        session.add(news)
        session.commit()
        return jsonify({'success': 'OK'})


# для общих запросов к постам
api.add_resource(NewsListResource, '/api/news')
# для запросов по индексу
api.add_resource(NewsResource, '/api/news/<int:news_id>')
