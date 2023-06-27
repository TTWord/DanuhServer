from service.shared_service import SharedService
from flask_restx import Namespace, Resource, Api, reqparse, fields
from util.decorator.authorization import Authorization


api = Namespace('share', description='공유 API')


@api.route("/userservice")
@api.doc(security="Bearer Auth")
class Shared(Resource):
    @api.response(200, "Success")
    @api.response(400, "Bad request")
    # @Authorization.reject_authorization
    def get(self):
        """
        전체 공유 단어장 가져오기
        """
        return SharedService.get_all_shared_books()

