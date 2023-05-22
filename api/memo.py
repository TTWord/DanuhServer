from flask_restx import Namespace, Resource, Api, reqparse, fields
from util.decorator.authorization import Authorization
from flask import request
from service.memo_service import MemoService


api = Namespace('memo', description='단어장 API')

@api.route("")
@api.doc(security='Bearer Auth')
class Memo(Resource):
    @api.doc(params={'count': '단어 개수', 'book_ids': '단어장 아이디(&로 구분)'})
    @Authorization.check_authorization
    def get(self, auth):
        """
        단어 암기( &로 구분)
        """
        count = request.args.get('count')
        book_ids = request.args.get('book_ids')
        book_ids = [int(book_id) for book_id in book_ids.split("&")]
        return MemoService.generate_memo_service(auth=auth, data={ 'book_ids': book_ids, 'count': int(count) })
    

    @api.doc(params={'word_id': '단어 ID', 'is_memorized': '암기 상태'})
    @Authorization.reject_authorization
    def patch(self):
        """
        단어 암기 상태 변경(토글 선택 및 해제 시)
        """
        word_id = request.args.get('word_id')
        is_memorized = request.args.get('is_memorized')
        return MemoService.update_memo_service(data={ 'word_id': word_id, 'is_memorized': is_memorized })