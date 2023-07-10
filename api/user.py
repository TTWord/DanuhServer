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
        ),
        "to_password2": fields.String(
            required=True, description="변경할 비밀번호 확인"
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

post_parser = api.parser()
post_parser.add_argument("file", type=FileStorage, location="files")


@api.route("/userservice")
@api.doc(security="Bearer Auth")
class User(Resource):
    @api.response(200, "Success")
    @api.response(400, "Bad request")
    @Authorization.check_authorization
    def get(self, auth):
        """
        유저 프로필 가져오기
        """
        return UserService.get_user_profile(auth)

    @api.response(200, "Success")
    @api.response(400, "Bad request")
    @api.expect(post_parser)
    @Authorization.check_authorization
    def post(self, auth):
        """
        유저 프로필 사진 수정
        """
        file = request.files["file"]
        return UserService.update_user_profile(auth, file)

    @api.response(200, "Success")
    @api.response(400, "Bad request")
    @Authorization.check_authorization
    def delete(self, auth):
        """
        유저이름으로 회원 탈퇴
        """
        return UserService.delete_user_by_username(auth)

    @api.response(200, "Success")
    @api.response(400, "Bad request")
    @api.expect(change_nickname, validate=True)
    @Authorization.check_authorization
    def put(self, auth):
        """
        유저 닉네임으로 닉네임 변경
        """
        input_data = request.get_json()
        return UserService.update_user_by_nickname(auth, input_data)


@api.route("/<int:id>")
@api.doc(security="Bearer Auth")
class UserById(Resource):
    def get(self, id):
        """
        유저 ID로 유저 조회
        """
        return UserService.get_user_by_id(id)

    @Authorization.reject_authorization
    @api.expect(change_password)
    def put(self, id):
        """
        유저 ID로 비밀번호 수정
        """
        data = request.get_json()

        return UserService.update_user(id=id, data=data)

    def delete(self, id):
        """
        유저 ID로 유저 삭제
        """
        return UserService.delete_user_by_id(id=id)
