from flask import Blueprint, request
from flask_restx import Namespace, Resource, Api
from services.user_service import signup_service, signin_service

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
        return signup_service(data)

@api.route('/signin')
class UserSignIn(Resource):
    def post(self):
        data = request.get_json()
        return signin_service(data)
