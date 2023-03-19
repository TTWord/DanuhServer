from service.book_service import BookService
from flask_restx import Namespace, Resource, Api, reqparse, fields
from util.decorator.authorization import Authorization
from flask import request


api = Namespace('book', description='단어장 API')

book_name = api.model('책 이름', {
    'name': fields.String(required=True, description='단어장 이름', example='단어장 이름')
})

generate_book = api.model('단어장 생성', {
    **book_name,
    'text': fields.String(required=True, description='예측 값 입력', example='You can tell a stranger that this is shiitake mushrooms.')
})

auth_header = api.parser()
auth_header.add_argument('Authorization', type=str, location='headers', required=True, help='Bearer Access Token')


@api.route("")
class Book(Resource):
    # @api.expect(getBookParser)
    @api.expect(auth_header)
    @Authorization.check_authorization
    def get(self, auth):
        """
        모든 단어장 조회
        """
        return BookService.get_books_by_user_id(auth)
    
    @api.expect(auth_header, book_name)
    @Authorization.check_authorization
    def post(self, auth):
        """
        단어장 추가
        """
        data = request.get_json()
        
        return BookService.add_book(auth, data)
    

@api.route('/<int:id>')
class BookById(Resource):
    @Authorization.check_authorization
    @api.expect(auth_header)
    def get(self, id, auth):
        """
        단어장 ID로 단어장 조회
        """
        return BookService.get_book_by_id(auth, id)
    
    @Authorization.check_authorization
    @api.expect(auth_header, book_name)
    def put(self, id, auth):
        """
        단어장 ID로 단어장 수정
        """
        data = request.get_json()
        
        return BookService.update_book(auth=auth, id=id, data=data)
    
    @Authorization.check_authorization
    @api.expect(auth_header)
    def delete(self, id, auth):
        """
        단어장 ID로 단어장 삭제
        """
        return BookService.delete_book(auth=auth, id=id)


@api.route('/generate')
class BookMaker(Resource):
    @api.expect(auth_header, generate_book)
    @Authorization.check_authorization
    def post(self, auth):
        """
        문장을 통해 단어장 추가
        """
        data = request.get_json()
        return BookService.generate_book(auth, data)