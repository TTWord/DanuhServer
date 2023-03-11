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
class WordByBook(Resource):
    # @Authorization.get_authorization
    @api.response(200, 'Success')
    def get(self):
        """
        모든 단어 조회
        """

        data = request.args
        return WordService.get_words_by_book_id(data)
    
    # @Authorization.get_authorization
    @api.response(200, 'Success')
    @api.expect(word_info)
    def post(self):
        """
        단어 추가
        """
        data = request.get_json()
        return WordService.add(data)
    

@api.route('/<int:id>')
class WordById(Resource):
    # @Authorization.get_authorization
    def get(self, id):
        """
        단어ID로 조회
        """
        return WordService.get_word_by_id(id)

    # @Authorization.get_authorization
    @api.expect(word_info)
    def put(self, id):
        """
        단어ID에 해당하는 단어 수정
        """
        data = request.get_json()
        return WordService.update(id, data)
    
    # @Authorization.get_authorization
    def delete(self, id):
        """
        단어ID에 해당하는 단어 삭제
        """ 
        return WordService.delete(id)