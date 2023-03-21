from flask import request
from flask_restx import Namespace, Resource, Api, reqparse, fields
from service.user_service import UserService


api = Namespace('user', description='유저 API')

user_name = api.model('유저이름', {
    'username': fields.String(required=True, description='아이디', example='kimjunghyun696@google.com')
})

user_sign_up = api.model('회원 가입', {
    **user_name,
    'password': fields.String(required=True, description='비밀번호', example='13131313'),
    'nickname': fields.String(required=True, description='닉네임', example='김흐긴'),
    'certification_id': fields.String(required=True, description='인증ID', example='474825')
})


@api.route('/signup')
class UserSignUp(Resource):
    @api.expect(user_sign_up, validate=True)
    @api.response(200, 'Success')
    @api.response(400, 'Bad request')
    def post(self):
        """
        회원 가입
        """
        input_data = request.get_json()
        return UserService.signup_service(input_data)
    
    @api.expect(user_name, validate=True)
    @api.response(200, 'Success')
    @api.response(400, 'Bad request') 
    def delete(self):
        """
        회원 탈퇴
        """
        input_data = request.get_json()
        return UserService.delete_service(input_data)