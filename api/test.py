from flask import request
from flask_restx import Namespace, Resource, Api, reqparse, fields
from service.auth_service import AuthService
from util.decorator.authorization import Authorization
from urllib.parse import urlencode
from flask import current_app, redirect, abort
from config import config
from flask import url_for


api = Namespace('oauth', description='TEST API(OAUTH)')

user_sign_in = api.model('회원 로그인', {
    'username': fields.String(required=True, description='아이디', example='kimjunghyun696@google.com'),
    'password': fields.String(required=True, description='비밀번호', example='a123456!'),
})

email_content = api.model('메일 인증', {
    **user_sign_in,
    'nickname': fields.String(required=True, description='닉네임', example='김흐긴'),
})


# import requests
# @api.route('/<target>')
# class OAuth(Resource):
#     @api.response(200, 'Success')
#     @api.response(400, 'Bad request')
#     def get(self, target):
#         """
#         awpoegjpwoeg
#         """
#         GOOGLE_DISCOVERY_URL = (
#             "https://accounts.google.com/.well-known/openid-configuration"
#         )
#         google_provider_cfg = requests.get(GOOGLE_DISCOVERY_URL).json()
#         authorization_endpoint = google_provider_cfg["authorization_endpoint"]
#         request_uri = client.prepare_request_uri(
#         authorization_endpoint,
#         redirect_uri=request.base_url + "/callback",
#         scope=["openid", "email", "profile"],
    # )
    # def get(self, target):
    #     # authorization code 받아오기
    #     if target not in ['google', 'kakao']:
    #         # error 발생시키기
    #         # return abort(404)
    #         print("1")

    #     target = str.upper(target)

    #     authorize_endpoint = config['REDIRECT_URI_SOCIAL']
    #     client_id = config[f'{target}_CLIENT_ID']
    #     redirect_uri = config[f'{target}_REDIRECT_URI']
    #     response_type = "code"
    #     scope = current_app.config.get(f'{target}_SCOPE')

    #     query_string = urlencode(dict(
    #         redirect_uri=redirect_uri,
    #         client_id=client_id,
    #         scope=scope,
    #         response_type=response_type
    #     ))

    #     authorize_redirect = f'{authorize_endpoint}?{query_string}'

    #     return redirect(authorize_redirect)
    
    # @api.response(200, 'Success')
    # @api.response(400, 'Bad request')
    # def post(self):
    #     """
    #     카카오 로그인
    #     """
    #     return AuthService.signin_with_kakao_service()
    

import requests
@api.route('<target>', methods=['GET'])
def authorize(target):
    # authorization code 받아오기
    if target not in ['google', 'kakao']:
        # error 발생시키기
        return abort(404)

    target = str.upper(target)

    authorize_endpoint = config['REDIRECT_URI']
    client_id = config['GOOGLE_CLIENT_ID']
    redirect_uri = config['REDIRECT_URI_SOCIAL']
    response_type = "code"
    scope = "openid email profile"

    query_string = urlencode(dict(
        redirect_uri=redirect_uri,
        client_id=client_id,
        scope=scope,
        response_type=response_type
    ))

    authorize_redirect = f'{authorize_endpoint}?{query_string}'

    return redirect(authorize_redirect)

@api.route('/oauth/callback/google', methods=['GET'])
def google_callback():
    code = request.args.get('code')
    token_endpoint = config['REDIRECT_URI']
    client_id = config['GOOGLE_CLIENT_ID']
    client_secret = config['GOOGLE_CLIENT_SECRET']
    redirect_uri = config['REDIRECT_URI_SOCIAL']
    grant_type = 'authorization_code'

    resp = requests.post(token_endpoint, data=dict(
        code=code,
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        grant_type=grant_type
    ))
    print(response)