from flask import request
from flask_restx import Namespace, Resource, Api, reqparse
from service.user_service import UserService

api = Namespace('user', description='유저 API')

parser = reqparse.RequestParser()


@api.route('/signup')
class UserSignUp(Resource):
    @api.doc(parser=parser)
    def post(self):
        args = parser.parse_args()
        parser.add_argument('username', type=str, help='유저 이름')
        parser.add_argument('password', type=str, help='비밀 번호')
        parser.add_argument('nickname', type=str, help='닉네임')
        username = args['username']
        password = args['password']
        nickname = args['nickname']

        data = {
            "username": username,
            "password": password,
            "nickname": nickname
        }
        return UserService.signup_service(data)


@api.route('/signin')
class UserSignIn(Resource):
    @api.doc(parser=parser)
    def post(self):
        args = parser.parse_args()
        username = args['username']
        password = args['password']

        data = {
            "username": username,
            "password": password,
        }
        return UserService.signin_service(data)
