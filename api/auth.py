from flask import request
from flask_restx import Namespace, Resource, Api, reqparse, fields
from service.auth_service import AuthService
from util.decorator.authorization import Authorization


api = Namespace('auth', description='관리 API')

user_sign_in = api.model('회원 로그인', {
    'username': fields.String(required=True, description='아이디', example='kimjunghyun696@google.com'),
    'password': fields.String(required=True, description='비밀번호', example='13131313'),
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
    @Authorization.check_authorization
    def post(self, auth):
        """
        액세스 토큰 재발급
        """
        return AuthService.get_new_access_token(auth)