from service.word_service import WordService
from flask_restx import Namespace, Resource, Api, reqparse, fields
from util.decorator.authorization import Authorization
from flask import request


api = Namespace('word', description='단어 API')

book_id = api.model('id', {
    'book_id': fields.Integer(required=True, description='단어장 ID', example=1)
})

word_info = api.model('추가 정보', {
    **book_id,
    'word': fields.String(required=True, description='단어', example='Eternal Return'),
    'mean': fields.String(required=True, description='의미', example='영원한 회귀'),
})


@api.route('')
@api.doc(security='Bearer Auth')
class WordByBook(Resource):
    @api.response(200, 'Success')
    @api.response(400, 'Fail')
    @Authorization.check_authorization
    def get(self, auth):
        """
        모든 단어 조회
        """

        data = request.args
        return WordService.get_words_by_book_id(data, auth)
    
    @api.response(200, 'Success')
    @api.response(400, 'Fail')
    @api.expect(word_info)
    @Authorization.check_authorization
    def post(self, auth):
        """
        단어 추가
        """
        data = request.get_json()
        return WordService.add(data, auth)
    

@api.route('/<int:id>')
@api.doc(security='Bearer Auth')
class WordById(Resource):
    @api.response(200, 'Success')
    @api.response(400, 'Fail')
    @api.expect(word_info)
    @Authorization.reject_authorization
    def get(self, id):
        """
        단어 ID로 단어 조회
        """
        return WordService.get_word_by_id(id)

    @api.response(200, 'Success')
    @api.response(400, 'Fail')
    @api.expect(word_info)
    @Authorization.check_authorization
    def put(self, id, auth):
        """
        단어 ID로 단어 수정
        """
        data = request.get_json()
        return WordService.update(id, data, auth)
    
    @api.response(200, 'Success')
    @api.response(400, 'Fail')
    @Authorization.check_authorization
    def delete(self, id, auth):
        """
        단어 ID로 단어 삭제
        """ 
        return WordService.delete(id, auth)