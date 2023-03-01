from flask import Blueprint, request
from flask_restx import Namespace, Resource, Api
from services.user_service import signup_service, login_service

api = Namespace('user', description='User related operations')

@api.route('/signup')
class UserSignUp(Resource):
    def post(self):
        data = request.get_json()
        return signup_service(data)

@api.route('/login')
class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        return login_service(data)
