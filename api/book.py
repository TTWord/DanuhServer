from flask import Blueprint
from services.book import get_book_service

book_route = Blueprint('book', __name__, url_prefix='/book')

@book_route.route('/', methods=['GET'])
def get_book():
    return get_book_service()