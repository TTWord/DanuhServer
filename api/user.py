from flask import request
from flask_restx import Namespace, Resource, Api, reqparse, fields
from werkzeug.datastructures import FileStorage
from service.user_service import UserService
from util.decorator.authorization import Authorization


api = Namespace("user", description="유저 API")

user_name = api.model(
    "유저이름",
    {
        "username": fields.String(
            required=True, description="아이디", example="kimjunghyun696@google.com"
        )
    },
)

change_nickname = api.model(
    "닉네임 변경",
    {
        "to_nickname": fields.String(
            required=True, description="변경할 닉네임", example="김흐긴4"
        ),
    },
)

change_password = api.model(
    "비밀번호 변경",
    {
        "from_password": fields.String(
            required=True, description="변경전 비밀번호"
        ),
        "to_password": fields.String(
            required=True, description="변경할 비밀번호"
        )
    },
)

user_sign_up = api.model(
    "회원 가입",
    {
        **user_name,
        "password": fields.String(
            required=True, description="비밀번호", example="a123456!"
        ),
        "nickname": fields.String(required=True, description="닉네임", example="김흐긴"),
        "certification_id": fields.String(
            required=True, description="인증ID", example="474825"
        ),
    },
)
user_sign_up = api.model(
    "회원 가입",
    {
        **user_name,
        "password": fields.String(
            required=True, description="비밀번호", example="a123456!"
        ),
        "nickname": fields.String(required=True, description="닉네임", example="김흐긴"),
        "certification_id": fields.String(
            required=True, description="인증ID", example="474825"
        ),
    },
)

require_info = api.model(
    "버그 신고",
    {
        "type": fields.String(
            required=True, description="유형", example="버그 신고"
        ),
        "contents": fields.String(
            required=True, description="내용", example="잘 안되요.."
        ),
    },
)

delete_info = api.model(
    "삭제 시 불편한 점",
    {
        "contents": fields.String(
            required=True, description="불만 사항", example="너무 느려요.."
        ),
    },
)

post_parser = api.parser()
post_parser.add_argument("file", type=FileStorage, location="files")


# TODO : 닉네임으로 조회하기 필요(상대방 프로필 보기)
# TODO : model 정리 필요
#       - 부가적인 정보에 따라서 많은 모델을 생성해야함
@api.route("/userservice")
@api.doc(security="Bearer Auth")
class User(Resource):
    @api.response(200, "SUCCESS")
    @api.response(500, "FAIL")
    @Authorization.check_authorization
    def get(self, auth):
        """
        유저 프로필 가져오기
        """
        return UserService.get_user_profile(auth)

    @api.response(200, "SUCCESS")
    @api.response(500, "FAIL")
    @api.expect(post_parser)
    @Authorization.check_authorization
    def post(self, auth):
        """
        유저 프로필 사진 수정
        """
        file = request.files["file"]
        return UserService.update_user_profile(auth, file)

    @api.response(200, "SUCCESS")
    @api.response(409, "USER_NOT_FOUND")
    @api.response(500, "FAIL")
    @Authorization.check_authorization
    def delete(self, auth):
        """
        유저이름으로 회원 탈퇴
        """
        return UserService.delete_user_by_username(auth)

    @api.response(200, "SUCCESS")
    @api.response(409, "USER_DUPLICATE_NICKNAME")
    @api.response(500, "FAIL")
    @api.expect(change_nickname, validate=True)
    @Authorization.check_authorization
    def put(self, auth):
        """
        유저 닉네임으로 닉네임 변경
        """
        input_data = request.get_json()
        return UserService.update_user_by_nickname(auth, input_data)
    
    @api.response(200, "SUCCESS")
    @api.response(409, "USER_NOT_FOUND, USER_INVALID_ACESSSS, USER_INVALID_FORMAT_PASSWORD, USER_SAME_PASSWORD")
    @api.response(500, "FAIL")
    @api.expect(change_password)
    @Authorization.check_authorization
    def patch(self, auth):
        """
        유저 ID로 비밀번호 수정
        """
        data = request.get_json()
        return UserService.update_user_password(auth=auth, data=data)


@api.route("/<int:id>")
@api.doc(security="Bearer Auth")
class UserById(Resource):
    @api.response(200, "SUCCESS")
    @api.response(409, "USER_NOT_FOUND")
    @api.response(500, "FAIL")
    def get(self, id):
        """
        유저 ID로 유저 조회
        """
        return UserService.get_user_by_id(id)
    
    @api.response(200, "SUCCESS")
    @api.response(409, "USER_NOT_FOUND")
    @api.response(500, "FAIL")
    def delete(self, id):
        """
        유저 ID로 유저 삭제
        """
        return UserService.delete_user_by_id(id=id)


@api.route("/profile/<int:id>")
@api.doc(security="Bearer Auth")
class OtherUser(Resource):
    @api.response(200, "SUCCESS")
    @api.response(409, "USER_NOT_FOUND")
    @api.response(500, "FAIL")
    def get(self, id):
        """
        상대 유저 프로필 보기
        """
        return UserService.get_another_user_profile(id)
    
    
@api.route("userservice/issue")
@api.doc(security="Bearer Auth")
class InputRequire(Resource):
    @api.response(200, "SUCCESS")
    @api.response(409, "USER_NOT_FOUND")
    @api.response(500, "FAIL")
    @api.expect(require_info)
    # @Authorization.check_authorization
    def post(self):
        """
        건의 사항/ 버그 신고
        """
        data = request.get_json()
        # type, string
        return UserService.report_to_danuh(data)
    

@api.route("/userservice/survey")
@api.doc(security="Bearer Auth")
class Survey(Resource):
    @api.response(200, "SUCCESS")
    @api.response(409, "USER_NOT_FOUND")
    @api.response(500, "FAIL")
    @api.expect(delete_info)
    # @Authorization.check_authorization
    def post(self):
        """
        탈퇴 시 불편한 점
        """
        data = request.get_json()
        # string
        return UserService.report_to_danuh(data)