from flask import Blueprint
from api.book import book_route
from api.word import word_route

main_route = Blueprint('main', __name__, url_prefix="/api")

main_route.register_blueprint(book_route, url_prefix='/book')
main_route.register_blueprint(word_route, url_prefix='/word')

@main_route.route('/', methods=['GET'])
def api():
    return 'API Ver.0.0.1'