from service.book_service import BookService
from flask_restx import Namespace, Resource
from util.decorator.authorization import Authorization
from flask import request

api = Namespace('book', description='단어장 API')

# getBookParser = api.parser()
# getBookParser.add_argument('name', type=str, help='단어장 이름', location='args')
    
@api.route("/")
class Book(Resource):
    # @api.expect(getBookParser)
    @Authorization.check_authorization
    def get(self, auth):
        """
        모든 단어장 조회
        설명입니다
        """
        return BookService.get_books_by_user_id(auth)
    
    @Authorization.check_authorization
    def post(self, auth):
        data = request.get_json()
        
        return BookService.add_book(auth, data)
    
@api.route('/<int:id>')
class BookById(Resource):
    @Authorization.check_authorization
    def get(self, id, auth):
        return BookService.get_book_by_id(auth, id)
    
    @Authorization.check_authorization
    def put(self, id, auth):
        data = request.get_json()
        
        return BookService.update_book(auth=auth, id=id, data=data)
    
    @Authorization.check_authorization
    def delete(self, id, auth):
        return BookService.delete_book(auth=auth, id=id)
