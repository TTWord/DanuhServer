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
            required=True, description="아이디", example="kimjunghyun696@gmail.com"
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

report_info = api.model(
    "버그 신고",
    {
        "type": fields.String(
            required=True, description="유형", example="버그 신고"
        ),
        "contents": fields.String(
            required=True, description="내용", example="잘 안되요.."
        )
    },
)

survey_info = api.model(
    "삭제 시 불편한 점",
    {
        "contents": fields.List(
            fields.String, required=True, description="불만 사항", example=["사용하기 불편함", "학습하기 불편함", "단어를 외우기 싫음", "더이상 사용하지 않음", "사용자가 직접 입력하는 텍스트"]
        )
    },
)

post_parser = api.parser()
post_parser.add_argument("file", type=FileStorage, location="files")


# TODO : 닉네임으로 조회하기 필요(상대방 프로필 보기)
# TODO : model 정리 필요
#       - 부가적인 정보에 따라서 많은 모델을 생성해탈퇴 설문조사 데이터
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
    
    
@api.route("/userservice/report")
@api.doc(security="Bearer Auth")
class Report(Resource):
    @api.response(200, "SUCCESS")
    @api.response(409, "USER_NOT_FOUND")
    @api.response(500, "FAIL")
    @api.expect(report_info)
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
    @api.expect(survey_info)
    # @Authorization.check_authorization
    def post(self):
        """
        탈퇴 시 불편한 점
        """
        data = request.get_json()
        # string
        return UserService.report_to_danuh(data)