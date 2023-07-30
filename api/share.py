from service.share_service import ShareService
from flask_restx import Namespace, Resource, Api, reqparse, fields
from util.decorator.authorization import Authorization
from flask import request


api = Namespace('share', description='공유 API')

share_info = api.model('공유 정보', {
    'id': fields.Integer(required=True, description='공유 ID', example=1)
})

update_share_info = api.model('수정할 공유 정보', {
    'type': fields.String(required=True, description='추가할 값(downloaded, checked)', example='downloaded')
})


@api.route("")
@api.doc(security="Bearer Auth")
class Share(Resource):
    @api.response(200, "SUCCESS")
    @api.response(500, "FAIL")
    @api.doc(params={'name': '이름 필터', 'type': 'downloaded, checked(기본 checked)',
                      'order': 'DESC, ASC(기본 DESC)'})
    @Authorization.reject_authorization
    def get(self):
        """
        공유 단어장 가져오기
        """
        name = request.args.get('name')
        type = request.args.get('type', default="checked", type=str)
        order = request.args.get('order', default="DESC", type=str)

        return ShareService.get_all_shared_books(data={'name': name, 'order': order, 'type': type})

    @api.response(200, "SUCCESS")
    @api.response(409, "SHARE_NOT_FOUND, SHARE_BOOK_OWNER, SHARE_ALREADY_EXIST")
    @api.response(500, "FAIL")
    @api.expect(share_info)
    @Authorization.check_authorization
    def post(self, auth):
        """
        공유 단어장 다운로드
        """
        data = request.get_json()
        return ShareService.download_book(auth=auth, data=data)


@api.route('/<int:id>')
@api.doc(security="Bearer Auth")
class ShareById(Resource):
    @api.response(200, "SUCCESS")
    @api.response(409, "SHARE_NOT_FOUND")
    @api.response(500, "FAIL")
    @Authorization.reject_authorization
    def get(self, id):
        """
        ID를 통해 조회
        """
        return ShareService.get_share_by_id(id)
    
    @api.response(200, "SUCCESS")
    @api.response(409, "SHARE_NOT_FOUND")
    @api.response(500, "FAIL")
    @Authorization.check_authorization
    def post(self, auth, id):
        """
        추천 하기, 취소
        """
        return ShareService.update_recommend_share(auth, id)


@api.route('/user')
@api.doc(security="Bearer Auth")
class ShareByUser(Resource):
    @api.response(200, "SUCCESS")
    @api.response(500, "FAIL")
    @api.doc(params={'name': '이름 필터', 'type': 'downloaded, checked(기본 checked)',
                    'order': 'DESC, ASC(기본 DESC)'})
    @Authorization.check_authorization
    def get(self, auth):
        """
        유저별 공유 단어장
        """
        name = request.args.get('name')
        type = request.args.get('type', default="checked", type=str)
        order = request.args.get('order', default="DESC", type=str)

        return ShareService.get_user_shared_books(auth=auth, data={'name': name, 'order': order, 'type': type})
    

@api.route('/user/<int:user_id>')
@api.doc(security="Bearer Auth")
class ShareByOtherUser(Resource):
    @api.response(200, "SUCCESS")
    @api.response(500, "FAIL")
    @api.doc(params={'type': 'downloaded, checked(기본 checked)',
                    'order': 'DESC, ASC(기본 DESC)'})
    @Authorization.reject_authorization
    def get(self, user_id):
        """
        다른 유저 공유 단어장 목록
        """
        type = request.args.get('type', default="checked", type=str)
        order = request.args.get('order', default="DESC", type=str)

        return ShareService.get_other_user_shared_books(id=user_id, data={'order': order, 'type': type})
    
