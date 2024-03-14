from flask import Blueprint
from flask_restx import Api
from api.book import api as book_ns
from api.word import api as word_ns
from api.user import api as user_ns
from api.auth import api as auth_ns
from api.memo import api as memo_ns
from api.quiz import api as quiz_ns
from api.share import api as share_ns
from api.test import api as test_ns


authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

main_route = Blueprint('main', __name__, url_prefix="/api")

api = Api(
    main_route,
    version='1.0.0',
    title='DanuhServer',
    contact='KimJungHyun',
    contact_email='kimjunghyun696@gmail.com',
    description="This is Danuh API Documentation.",
    authorizations=authorizations
)

api.add_namespace(book_ns)
api.add_namespace(word_ns)
api.add_namespace(user_ns)
api.add_namespace(auth_ns)
api.add_namespace(memo_ns)
api.add_namespace(quiz_ns)
api.add_namespace(share_ns)
api.add_namespace(test_ns)