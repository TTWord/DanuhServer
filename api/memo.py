from flask_restx import Namespace, Resource, Api, reqparse, fields
from util.decorator.authorization import Authorization
from flask import request
from service.memo_service import MemoService


api = Namespace('memo', description='메모 API')

word_info = api.model('단어 정보', {
    'word_id': fields.Integer(required=True, description='풀이 개수', example=10),
    'is_memorized': fields.Boolean(required=False, description='암기 여부', example=False)
})

memo_info = api.model('암기 정보', {
    'book_ids': fields.String(required=True, description='단어장 ID', example="19&21"),
    'count': fields.Integer(required=True, description='풀이 개수', example=10)
})


@api.route("")
@api.doc(security='Bearer Auth')
class Memo(Resource):
    @api.expect(word_info)
    @Authorization.reject_authorization
    def patch(self):
        """
        단어 암기 상태 변경(토글 선택 및 해제 시)
        """
        data = request.get_json()
        return MemoService.update_memo_service(data=data)
    

@api.route("/flashcard")
@api.doc(security='Bearer Auth')
class FlashCardMemo(Resource):
    @api.expect(memo_info)
    @Authorization.check_authorization
    def post(self, auth):
        """
        플래시 카드 암기 생성
        """
        data = request.get_json()

        return MemoService.generate_flash_memo_service(auth=auth, data=data)
    

@api.route("/blind")
@api.doc(security='Bearer Auth')
class BlindMemo(Resource):
    @api.expect(memo_info)
    @Authorization.check_authorization
    def post(self, auth):
        """
        블라인드 암기 생성
        """
        data = request.get_json()
        
        return MemoService.generate_blind_memo_service(auth=auth, data=data)