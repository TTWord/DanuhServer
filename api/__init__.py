from flask import Blueprint
from flask_restx import Api
from api.book import api as book_ns
from api.word import api as word_ns
from api.user import api as user_ns


main_route = Blueprint('main', __name__, url_prefix="/api")

api = Api(
    main_route,
    version='0.3.0',
    title='TTWordServer',
    contact='KimJungHyun',
    contact_email='kimjunghyun696@gmail.com',
    description="This is TTWord API Documentation.",
)

api.add_namespace(book_ns)
api.add_namespace(word_ns)
api.add_namespace(user_ns)