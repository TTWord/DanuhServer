from flask import request
from flask_restx import Namespace, Resource, Api, reqparse, fields
from service.user_service import UserService

api = Namespace('user', description='유저 API')

user_sign_in = api.model('회원 로그인', {
    'username': fields.String(required=True, description='아이디를 입력해주세요.', example='afsd721@google.com'),
    'password': fields.String(required=True, description='비밀번호를 입력해주세요.', example='13131313'),
})

user_sign_up = api.model('회원 가입', {
    **user_sign_in,
    'nickname': fields.String(required=True, description='닉네임을 입력해주세요.', example='김흐긴')
})

# from flask import make_response

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

        username = input_data['username']
        password = input_data['password']
        nickname = input_data['nickname']

        data = {
            "username": username,
            "password": password,
            "nickname": nickname
        }
        return UserService.signup_service(data)
    

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
        username = input_data['username']
        password = input_data['password']

        data = {
            "username": username,
            "password": password,
        }
        return UserService.signin_service(data)