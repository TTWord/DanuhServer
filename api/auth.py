from flask import request
from flask_restx import Namespace, Resource, Api, reqparse, fields
from service.auth_service import AuthService
from util.decorator.authorization import Authorization, RefreshToken


api = Namespace('auth', description='관리 API')

user_sign_in = api.model('회원 로그인', {
    'username': fields.String(required=True, description='아이디', example='kimjunghyun696@google.com'),
    'password': fields.String(required=True, description='비밀번호', example='a123456!'),
})

email_content = api.model('메일 인증', {
    **user_sign_in,
    'nickname': fields.String(required=True, description='닉네임', example='김흐긴'),
})


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
    @RefreshToken.check_authorization
    def post(self, auth):
        """
        액세스 토큰 재발급
        """
        return AuthService.get_new_access_token(auth)
    
    
@api.route('/<service>')
class OAuth(Resource):
    @api.response(200, 'Success')
    @api.response(400, 'Bad request')
    def get(self, service):
        """
        소셜 로그인 정보 전달(백엔드 정보 전달용)
        """
        code = request.args.get('code')
        return AuthService.social_auth_api(service, code)
    
    @api.response(200, 'Success')
    @api.response(400, 'Bad request')
    def post(self, service):
        """
        소셜 로그인
        """
        return AuthService.signin_with_social_service(service)
    