from service.book_service import BookService
from flask_restx import Namespace, Resource, Api, reqparse, fields
from util.decorator.authorization import Authorization
from flask import request


api = Namespace('book', description='단어장 API')

book_name = api.model('책 이름', {
    'name': fields.String(required=True, description='단어장 이름', example='단어장 이름')
})

book_info = api.model('단어장 생성', {
    **book_name,
    'text': fields.String(required=True, description='예측 값 입력', example='You can tell a stranger that this is shiitake mushrooms.')
})

book_share = api.model('공유 설정', {
    'id': fields.Integer(required=True, description='단어장 ID', example=1),
    'comment': fields.String(description='공유 단어장 설명', example='string')
})


# TODO : model 정리 필요
#       - 부가적인 정보에 따라서 많은 모델을 생성해야함
@api.route("")
@api.doc(security='Bearer Auth')
class Book(Resource):
    @Authorization.check_authorization
    def get(self, auth):
        """
        모든 단어장 조회
        """
        return BookService.get_books_by_user_id(auth)
    
    @api.expect(book_name)
    @Authorization.check_authorization
    def post(self, auth):
        """
        단어장 추가
        """
        data = request.get_json()
        
        return BookService.add_book(auth, data)
    

@api.route('/<int:id>')
@api.doc(security='Bearer Auth')
class BookById(Resource):
    @Authorization.check_authorization
    def get(self, id, auth):
        """
        단어장 ID로 단어장 조회
        """
        return BookService.get_book_by_id(auth, id)
    
    @Authorization.check_authorization
    @api.expect(book_name)
    def put(self, id, auth):
        """
        단어장 ID로 단어장 수정
        """
        data = request.get_json()
        
        return BookService.update_book(auth=auth, id=id, data=data)
    
    @Authorization.check_authorization
    def patch(self, id, auth):
        """
        공유 단어장 업데이트
        """        
        return BookService.update_share_book(auth=auth, id=id)
    
    @Authorization.check_authorization
    def delete(self, id, auth):
        """
        단어장 ID로 단어장 삭제
        """
        return BookService.delete_book(auth=auth, id=id)


@api.route('/generate')
@api.doc(security='Bearer Auth')
class BookMaker(Resource):
    @api.expect(book_info)
    @Authorization.check_authorization
    def post(self, auth):
        """
        문장을 통해 단어장 추가
        """
        data = request.get_json()
        return BookService.generate_book(auth, data)


@api.route('/share')
@api.doc(security='Bearer Auth')
class BookShare(Resource):
    @api.expect(book_share)
    @Authorization.check_authorization
    def post(self, auth):
        """
        단어장 공개
        """
        data = request.get_json()
        return BookService.add_share_book(auth, data)
    
    @api.expect(book_share)
    @Authorization.check_authorization
    def delete(self, auth):
        """
        단어장 비공개
        """
        data = request.get_json()
        return BookService.delete_share_book(auth, data)
    