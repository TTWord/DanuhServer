from flask_restx import Namespace, Resource, Api, reqparse, fields
from util.decorator.authorization import Authorization
from flask import request
from service.memo_service import MemoService


api = Namespace('memo', description='메모 API')

memo_info = api.model('메모 정보', {
    'word_id': fields.Integer(required=True, description='풀이 개수', example=10),
    'is_memorized': fields.Boolean(required=False, description='암기 여부', example=False)
})


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
    

    @api.expect(memo_info)
    @Authorization.reject_authorization
    def patch(self):
        """
        단어 암기 상태 변경(토글 선택 및 해제 시)
        """
        data = request.get_json()
        return MemoService.update_memo_service(data=data)