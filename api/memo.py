from flask_restx import Namespace, Resource, Api, reqparse, fields
from util.decorator.authorization import Authorization
from flask import request
from service.memo_service import MemoService


api = Namespace('memo', description='단어장 API')

@api.route("/<int:book_id>")
@api.doc(security='Bearer Auth')
class Memo(Resource):
    @api.doc(params={'count': '단어 개수'})
    @Authorization.check_authorization
    def get(self, book_id, auth):
        """
        단어 암기
        """
        count = request.args.get('count')
        return MemoService.memo_service(auth=auth, data={ 'book_id': book_id, 'count': int(count) })