from flask import request
from flask_restx import Namespace, Resource, Api, reqparse, fields
from service.auth_service import AuthService
from util.decorator.authorization import Authorization, RefreshToken


api = Namespace("auth", description="관리 API")

user_name = api.model(
    "유저이름",
    {
        "username": fields.String(required=True, description="아이디", example="kimjunghyun696@google.com")
    }
)

user_sign_in = api.model(
    "회원 로그인",
    {
        "username": fields.String(required=True, description="아이디", example="kimjunghyun696@google.com"),
        "password": fields.String(required=True, description="비밀번호", example="a123456!"),
    }
)

email_content = api.model(
    "메일 인증",
    {
        **user_sign_in,
        "nickname": fields.String(required=True, description="닉네임", example="김흐긴"),
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

nickname = api.model(
    "닉네임 중복 확인",
    {

        "nickname": fields.String(required=True, description="닉네임", example="김흐긴")
    },
)

cert_key = api.model(
    "인증키",
    {
        **user_name,
        "certification_id": fields.String(
            required=True, description="인증ID", example="474825"
        )
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

change_password_for_unlogin = api.model(
    "비로그인 회원에 대한 비밀번호 변경",
    {
        **user_name,
        "certification_id": fields.String(
            required=True, description="인증ID", example="474825"
        ),
        "to_password": fields.String(
            required=True, description="변경할 비밀번호"
        )
    },
)

# TODO : model 정리 필요
#       - 부가적인 정보에 따라서 많은 모델을 생성해야함
@api.route("/signin")
class UserSignIn(Resource):
    @api.expect(user_sign_in, validate=True)
    @api.response(200, "SUCCESS")
    @api.response(409, "USER_NOT_FOUND, AUTH_ACCESS_FAILD")
    @api.response(500, "FAIL")
    def post(self):
        """
        로그인
        """
        input_data = request.get_json()
        return AuthService.signin_service(input_data)


@api.route("/check/nickname")
class CheckNickname(Resource):
    @api.expect(nickname, validate=True)
    @api.response(200, "SUCCESS")
    @api.response(409, "USER_INVALID_USERNAME, USER_DUPLICATE_NICKNAME")
    @api.response(500, "FAIL")
    def post(self):
        """
        닉네임 중복 확인
        """
        data = request.get_json()

        return AuthService.check_nickname(data)


@api.route("/sendmail")
class SendMail(Resource):
    @api.expect(email_content, validate=True)
    @api.response(200, "SUCCESS")
    @api.response(409, "USER_DUPLICATE_USERNAME, USER_INVALID_FORMAT_USERNAME, USER_INVALID_FORMAT_PASSWORD")
    @api.response(500, "FAIL")
    def post(self):
        """
        인증 메일 전송
        """
        input_data = request.get_json()
        return AuthService.send_mail(input_data)


@api.route("/signup")
class UserSignUp(Resource):
    @api.response(200, "SUCCESS")
    @api.response(403, "AUTH_EXPIRED_CODE, AUTH_INCORRECT_CODE")
    @api.response(500, "FAIL")
    @api.expect(user_sign_up, validate=True)
    def post(self):
        """
        회원 가입
        """
        input_data = request.get_json()
        return AuthService.signup_service(input_data)


@api.route("/refreshtoken")
@api.doc(security="Bearer Auth")
class RefreshToken(Resource):
    @api.response(200, "SUCCESS")
    @api.response(500, "FAIL")
    @RefreshToken.check_authorization
    def post(self, auth):
        """
        액세스 토큰 재발급
        """
        return AuthService.get_new_access_token(auth)

@api.route("/apple/redirect")
class OAuthApple(Resource):
    @api.response(200, "SUCCESS")
    @api.response(409, "AUTH_ACCESS_FAILD, USER_ALREADY_REGISTERED")
    @api.response(500, "FAIL")
    def post(self):
        """
        소셜 로그인 정보 전달(백엔드 정보 전달용)
        """
        
        print(request.form)
        code = request.form["code"]
        return AuthService.social_auth_apple_api(code)

@api.route("/<service>")
class OAuth(Resource):
    @api.response(200, "SUCCESS")
    @api.response(409, "AUTH_ACCESS_FAILD, USER_ALREADY_REGISTERED")
    @api.response(500, "FAIL")
    def get(self, service):
        """
        소셜 로그인 정보 전달(백엔드 정보 전달용)
        """
        code = request.args.get("code")
        return AuthService.social_auth_api(service, code)

    @api.response(200, "SUCCESS")
    @api.response(500, "FAIL")
    def post(self, service):
        """
        소셜 로그인
        """
        return AuthService.signin_with_social_service(service)
    

@api.route("/findpassword")
class FindPassword(Resource):
    @api.response(200, "SUCCESS")
    @api.response(500, "FAIL")
    @api.response(409, "USER_INVALID_USERNAME, USER_INVALID_FORMAT_USERNAME, USER_SOCIAL_LOGIN")
    @api.expect(user_name, validate=True)
    def post(self):
        """
        비밀번호 찾기
        """
        input_data = request.get_json()
        return AuthService.send_mail_find_password(input_data)


@api.route("/findpassword/login")
@api.doc(security="Bearer Auth")
class Login(Resource):
    @api.response(200, "SUCCESS")
    @api.response(409, "USER_NOT_FOUND, USER_INVALID_ACESSSS, USER_INVALID_FORMAT_PASSWORD, USER_SAME_PASSWORD")
    @api.response(500, "FAIL")
    @api.expect(change_password)
    @Authorization.check_authorization
    def patch(self, auth):
        """
        비밀번호 수정
        """
        data = request.get_json()
        return AuthService.update_user_password(auth=auth, data=data)


@api.route("/findpassword/notlogin")
class NotLogin(Resource):
    @api.response(200, "SUCCESS")
    @api.response(409, "USER_INVALID_ACESSSS, USER_INVALID_FORMAT_PASSWORD, USER_SAME_PASSWORD")
    @api.response(500, "FAIL")
    @api.expect(change_password_for_unlogin)
    def patch(self):
        """
        비로그인 유저에 대한 비밀번호 수정
        """
        data = request.get_json()
        return AuthService.update_notlogin_password(data=data)


@api.route("/checkcert")
class CheckCert(Resource):
    @api.response(200, "SUCCESS")
    @api.response(500, "FAIL")
    @api.response(403, "AUTH_EXPIRED_CODE, AUTH_INCORRECT_CODE")
    @api.expect(cert_key, validate=True)
    def post(self):
        """
        인증키 검증
        """
        input_data = request.get_json()
        return AuthService.validation_key(input_data)