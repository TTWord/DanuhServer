from service.share_service import ShareService
from flask_restx import Namespace, Resource, Api, reqparse, fields
from util.decorator.authorization import Authorization
from flask import request
import json


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
    @api.doc(params={'name': '이름 필터', 'type': 'popularity, downloaded, updated_at(기본 updated_at)',
                    'order': 'DESC, ASC(기본 DESC)'})
    @Authorization.reject_authorization
    def get(self):
        """
        공유 단어장 가져오기
        """
        name = request.args.get('name')
        order = request.args.get('order', default="DESC", type=str)
        type = request.args.get('type', default="updated_at", type=str)

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
    @Authorization.check_authorization
    def get(self, auth, id):
        """
        ID를 통해 조회
        """
        return ShareService.get_share_by_id(auth, id)
    
    @api.response(200, "SUCCESS")
    @api.response(409, "SHARE_NOT_FOUND")
    @api.response(500, "FAIL")
    @Authorization.check_authorization
    def post(self, auth, id):
        """
        추천 하기, 취소
        """
        return ShareService.update_recommend_share(auth, id)


@api.route('/user/share')
@api.doc(security="Bearer Auth")
class ShareByUserShare(Resource):
    @api.response(200, "SUCCESS")
    @api.response(500, "FAIL")
    @api.doc(params={'type': 'updated_at',
                    'order': 'DESC, ASC(기본 DESC)'})
    @Authorization.check_authorization
    def get(self, auth):
        """
        유저별 공유 단어장
        """
        order = request.args.get('order', default="DESC", type=str)
        type = request.args.get('type', default="updated_at", type=str)

        return ShareService.get_user_shared_books(auth=auth, data={'order': order, 'type': type})


@api.route('/user/download')
@api.doc(security="Bearer Auth")
class ShareByUserDownload(Resource):
    @api.response(200, "SUCCESS")
    @api.response(500, "FAIL")
    @api.doc(params={'type': 'updated_at(기본 updated_at)', 'filter': '추천 단어장 필터링(기본 true)',
                    'order': 'DESC, ASC(기본 DESC)'})
    @Authorization.check_authorization
    def get(self, auth):
        """
        유저별 다운로드 단어장
        """
        type = request.args.get('type', default="updated_at", type=str)
        order = request.args.get('order', default="DESC", type=str)
        filter = True if str(request.args.get('filter', default="false", type=str)) == "true" else False

        return ShareService.get_user_downloaded_books(auth=auth, data={'filter': filter, 'order': order, 'type': type})
    
    
@api.route('/user/<int:user_id>')
@api.doc(security="Bearer Auth")
class ShareByOtherUser(Resource):
    @api.response(200, "SUCCESS")
    @api.response(500, "FAIL")
    @api.response(500, "FAIL")
    @api.doc(params={'type': 'popularity, downloaded, updated_at(기본 updated_at)',
                    'order': 'DESC, ASC(기본 DESC)'})
    @Authorization.reject_authorization
    def get(self, user_id):
        """
        다른 유저 공유 단어장 목록
        """
        order = request.args.get('order', default="DESC", type=str)
        type = request.args.get('type', default="updated_at", type=str)

        return ShareService.get_other_user_shared_books(id=user_id, data={'order': order, 'type': type})
    

@api.route('/update/<int:id>')
@api.doc(security="Bearer Auth")
class ShareByUserShare(Resource):
    @api.response(200, "SUCCESS")
    @api.response(404, "BOOKSHARE_NOT_FOUND, SHARE_NOT_FOUND")
    @api.response(409, "BOOK_ALREAY_UPDATED, SHARE_NOT_SHARED, BOOK_NOT_DOWNLOADED")
    @api.response(500, "FAIL")
    @Authorization.check_authorization
    def post(self, auth, id):
        """
        유저가 공유 받은 단어장 업데이트
        """
        return ShareService.update_share_book(auth, id)