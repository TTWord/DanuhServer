from flask import request
from flask_restx import Namespace, Resource, Api
from service.user_service import UserService

api = Namespace('user', description='유저 API')

@api.route('/signup')
class UserSignUp(Resource):
    def post(self):
        # data = request.get_json()
        data = {
            "username": "username",
            "password": "password",
            "nickname": "nickname"
        }
        return UserService.signup_service(data)


@api.route('/signin')
class UserSignIn(Resource):
    def post(self):
        # data = request.get_json()
        data = {
            "username": "username",
            "password": "password",
            "nickname": "nickname"
        }
        return UserService.signin_service(data)
