from flask import request
from flask_restx import Resource
from services.book import get_book_service
from flask_restx import Namespace, Resource, Api
from typing import Dict, Tuple


api = Namespace('user', description='Book related operations')


@api.route('/login')
class UserLogin(Resource):
    """
        User Login Resource
    """
    @api.doc('user login')
    # @api.expect(user_auth, validate=True)
    def post(self) -> Tuple[Dict[str, str], int]:
        # get the post data
        post_data = request.json
        return Auth.login_user(data=post_data)


@api.route('/logout')
class LogoutAPI(Resource):
    """
    Logout Resource
    """
    @api.doc('logout a user')
    def post(self) -> Tuple[Dict[str, str], int]:
        # get auth token
        auth_header = request.headers.get('Authorization')
        return Auth.logout_user(data=auth_header)
