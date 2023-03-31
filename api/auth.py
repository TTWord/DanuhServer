from flask import request, current_app
from flask_restx import Namespace, Resource, Api, reqparse, fields
from service.auth_service import AuthService
from util.decorator.authorization import Authorization
from authlib.integrations.flask_client import OAuth

api = Namespace('auth', description='관리 API')

user_sign_in = api.model('회원 로그인', {
    'username': fields.String(required=True, description='아이디', example='kimjunghyun696@google.com'),
    'password': fields.String(required=True, description='비밀번호', example='a123456!'),
})

email_content = api.model('메일 인증', {
    **user_sign_in,
    'nickname': fields.String(required=True, description='닉네임', example='김흐긴'),
})

oauth = OAuth(current_app)


@api.route('/signin')
class UserSignIn(Resource):
    @api.expect(user_sign_in, validate=True)
    @api.response(200, 'Success')
    @api.response(400, 'Bad request')
    def post(self):
        """
        로그인
        """
        input_data = request.get_json()
        return AuthService.signin_service(input_data)
        

@api.route('/sendmail')
class SendMail(Resource):
    @api.expect(email_content, validate=True)
    @api.response(200, 'Success')
    @api.response(400, 'Bad request')
    def post(self):
        """
        인증 메일 전송
        """
        input_data = request.get_json()
        return AuthService.send_mail(input_data)
    

@api.route('/refreshtoken')
@api.doc(security='Bearer Auth')
class RefreshToken(Resource):
    @api.response(200, 'Success')
    @api.response(400, 'Bad request')
    @Authorization.check_authorization
    def post(self, auth):
        """
        액세스 토큰 재발급
        """
        return AuthService.get_new_access_token(auth)
    

@api.route('/kakao')
class Kakaoauth(Resource):
    @api.response(200, 'Success')
    @api.response(400, 'Bad request')
    def get(self):
        """
        카카오 로그인 정보 전달
        """
        code = request.args.get('code')
        return AuthService.kakao_auth_api(code)
    
    @api.response(200, 'Success')
    @api.response(400, 'Bad request')
    def post(self):
        """
        카카오 로그인
        """
        return AuthService.signin_with_kakao_service()
    
@api.route('/google')
class Kakaoauth(Resource):
    @api.response(200, 'Success')
    @api.response(400, 'Bad request')
    def get(self):
        """
        구글 로그인 정보 전달
        """
        return AuthService.google_auth_api(oauth)
    
    @api.response(200, 'Success')
    @api.response(400, 'Bad request')
    def post(self):
        """
        구글 로그인
        """
        return AuthService.signin_with_google_service(oauth)
    