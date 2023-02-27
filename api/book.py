from services.book import get_book_service
from flask_restx import Namespace, Resource, Api


api = Namespace('books', description='Book related operations')

@api.route('')
class Book(Resource):
    def get(self):
        return get_book_service()
    
    def post(self):
        return "add_book"
    
@api.route('/<int:id>')
class BookById(Resource):
    def put(self, id):
        return "update_book"
    
    def delete(self, id):
        return "delete_book"
    
    
    