from flask import request
from flask_restx import Namespace, Resource, Api, reqparse, fields
from service.user_service import UserService


api = Namespace('user', description='유저 API')

user_name = api.model('유저이름', {
    'username': fields.String(required=True, description='아이디', example='kimjunghyun696@google.com')
})

user_sign_in = api.model('회원 로그인', {
    **user_name,
    'password': fields.String(required=True, description='비밀번호', example='13131313'),
})

user_sign_up = api.model('회원 가입', {
    **user_sign_in,
    'nickname': fields.String(required=True, description='닉네임', example='김흐긴'),
    'certification_id': fields.String(required=True, description='인증ID', example='077 255')
})

email_content = api.model('이메일 인증', {
    'to_email': fields.String(required=True, description='수신자 이메일 주소', example= 'djsk721@naver.com')
})


@api.route('/signup')
class UserSignUp(Resource):
    @api.expect(user_sign_up, validate=True)
    @api.response(200, 'Success')
    @api.response(403, 'Not forbbiden')
    @api.response(404, 'Not found')
    @api.response(405, 'Not allowed')
    @api.response(400, 'Bad request')
    @api.response(409, 'User already exists')
    def post(self):
        """
        회원 가입
        """
        input_data = request.get_json()
        return UserService.signup_service(input_data)
    
    @api.expect(user_name, validate=True)
    @api.response(200, 'Success')
    @api.response(403, 'Not forbbiden')
    @api.response(404, 'Not found')
    @api.response(405, 'Not allowed')
    @api.response(400, 'Bad request')
    @api.response(409, 'User already exists')   
    def delete(self):
        """
        회원 탈퇴
        """
        input_data = request.get_json()
        return UserService.delete_service(input_data)
    

@api.route('/signin')
class UserSignIn(Resource):
    @api.expect(user_sign_in, validate=True)
    @api.response(200, 'Success')
    @api.response(403, 'Not forbbiden')
    @api.response(404, 'Not found')
    @api.response(405, 'Not allowed')
    @api.response(400, 'Bad request')
    def post(self):
        """
        로그인
        """
        input_data = request.get_json()
        return UserService.signin_service(input_data)
        

@api.route('/sendmail')
class SendMail(Resource):
    @api.expect(email_content, validate=True)
    @api.response(200, 'Success')
    @api.response(403, 'Not forbbiden')
    @api.response(404, 'Not found')
    @api.response(405, 'Not allowed')
    @api.response(400, 'Bad request')
    @api.response(200, 'Success')
    @api.response(404, 'Login Failed')
    def post(self):
        """
        인증 메일 전송
        """
        input_data = request.get_json()
        return UserService.send_mail(input_data)