from service.word_service import WordService
from flask_restx import Namespace, Resource, Api, reqparse, fields
from util.decorator.authorization import Authorization
from flask import request
from util.decorator.logging import logging


api = Namespace('word', description='단어 API')

word_info = api.model('추가 정보', {
    'word': fields.String(required=True, description='단어', example='Eternal Return'),
    'mean': fields.String(required=True, description='의미', example='영원한 회귀'),
})


@api.route('/<int:book_id>')
@api.doc(security='Bearer Auth')
class WordByBook(Resource):
    @api.response(200, "SUCCESS")
    @api.response(403, "BOOK_ACCESS_DENIED")
    @api.response(409, "BOOK_NOT_FOUND")
    @api.response(500, "FAIL")
    @logging
    @Authorization.check_authorization
    def get(self, book_id, auth):
        """
        모든 단어 조회
        """
        return WordService.get_words_by_book_id(book_id, auth)
    
    @api.response(200, "SUCCESS")
    @api.response(400, "WORD_COUNT_MORE_THAN_LIMIT")
    @api.response(409, "WORD_INVALID_INPUT, WORD_MORE_THAN_LIMIT, BOOK_NOT_FOUND, BOOK_ACCESS_DENIED, BOOK_DOWNLOADED, WORD_ALREADY_EXIST")
    @api.response(500, "FAIL")
    @api.expect(word_info)
    @logging
    @Authorization.check_authorization
    def post(self, book_id, auth):
        """
        단어장에 단어 추가
        """
        data = request.get_json()
        return WordService.add(book_id, data, auth)
    

@api.route('/id/<int:id>')
@api.doc(security='Bearer Auth')
class WordById(Resource):
    @api.response(200, "SUCCESS")
    @api.response(409, "BOOK_NOT_FOUND")
    @api.response(500, "FAIL")
    @logging
    @Authorization.reject_authorization
    def get(self, id):
        """
        단어 ID로 단어 조회
        """
        return WordService.get_word_by_id(id)
    
    @api.response(200, "SUCCESS")
    @api.response(400, "WORD_COUNT_MORE_THAN_LIMIT")
    @api.response(403, "BOOK_ACCESS_DENIED")
    @api.response(409, "WORD_NOT_FOUND, BOOK_IS_DOWNLOADED, WORD_INVALID_INPUT")
    @api.response(500, "FAIL")
    @api.expect(word_info)
    @logging
    @Authorization.check_authorization
    def put(self, id, auth):
        """
        단어 ID로 단어 수정
        """
        data = request.get_json()
        return WordService.update(id, data, auth)
    
    @api.response(200, "SUCCESS")
    @api.response(403, "BOOK_ACCESS_DENIED")
    @api.response(404, "WORD_NOT_FOUND")
    @api.response(409, "BOOK_IS_DOWNLOADED")
    @api.response(500, "FAIL")
    @logging
    @Authorization.check_authorization
    def delete(self, id, auth):
        """
        단어 ID로 단어 삭제
        """ 
        return WordService.delete(id, auth)