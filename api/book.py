from services.book import get_book_service
from flask_restx import Namespace, Resource, Api


api = Namespace('books', description='Book related operations')

@api.route('')
class Book(Resource):
    def get(self):
        return get_book_service()
    