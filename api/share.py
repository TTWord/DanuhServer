from service.share_service import ShareService
from flask_restx import Namespace, Resource, Api, reqparse, fields
from util.decorator.authorization import Authorization
from flask import request


api = Namespace('share', description='공유 API')


# TODO : 쿼리 파라미터를 통해 여러 조건들을 추가
#       1. 이름
#       2. 정렬
@api.route("")
@api.doc(security="Bearer Auth")
class Share(Resource):
    @api.doc(params={'name': '이름 필터', 'type': 'downloaded, checked(기본 check)',
                      'order': 'DESC, ASC(기본 DESC)'})
    @api.response(200, "Success")
    @api.response(400, "Bad request")
    # @Authorization.reject_authorization
    def get(self):
        """
        공유 단어장 가져오기
        """
        name = request.args.get('name')
        order = request.args.get('order')
        type = request.args.get('type')

        return ShareService.get_all_shared_books(data={'name': name, 'order': order, 'type': type})


@api.route('/<int:id>')
@api.doc(security="Bearer Auth")
class ShareById(Resource):
    @api.response(200, "Success")
    @api.response(400, "Bad request")
    # @Authorization.reject_authorization
    def get(self, id):
        """
        ID를 통해 조회
        """
        return ShareService.get_share_by_id(id)
    
