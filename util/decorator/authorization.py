from flask import make_response, request
from util.jwt_token import decode_token
import jwt
from config import config
from functools import wraps
from util.custom_response import custom_response
from util.exception import CustomException


class Authorization:
    @staticmethod
    def check_authorization(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                access_token = request.headers.get('Authorization')
                if not access_token:
                    raise CustomException("액세스 토큰이 제공되지 않았습니다.", 401)
            
                token_info = access_token.split(" ")
                access_token = token_info[1]

                payload = decode_token(access_token, config["SECRET_KEY"])
                return func(auth = payload, *args, **kwargs)
            except jwt.ExpiredSignatureError:
                return custom_response("만료된 액세스 토큰입니다.", code=401)
            except jwt.InvalidTokenError:
                return custom_response("유효하지 않은 액세스 토큰입니다.", code=401)
            except CustomException as e:
                return e.get_response()
            except Exception as e:
                return custom_response("FAIL", code=500)

        return wrapper
            
    @staticmethod
    def get_authorization(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                access_token = request.headers['Authorization']
                
                token_info = access_token.split(" ")
                access_token = token_info[1]
                payload = decode_token(access_token, config["SECRET_KEY"])
                return func(auth = payload, *args, **kwargs)
            except jwt.ExpiredSignatureError:
                return custom_response("만료된 액세스 토큰입니다.", code=401)
            except Exception as e:
                return func(auth = None, *args, **kwargs)
        return wrapper
    
    @staticmethod
    def reject_authorization(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                access_token = request.headers.get('Authorization')
                if not access_token:
                    raise CustomException("액세스 토큰이 제공되지 않았습니다.", 401)
            
                token_info = access_token.split(" ")
                access_token = token_info[1]

                decode_token(access_token, config["SECRET_KEY"])
                return func(*args, **kwargs)
            except jwt.ExpiredSignatureError:
                return custom_response("만료된 액세스 토큰입니다.", code=401)
            except jwt.InvalidTokenError:
                return custom_response("유효하지 않은 액세스 토큰입니다.", code=401)
            except CustomException as e:
                return e.get_response()
            except Exception as e:
                return custom_response("FAIL", code=500)
        return wrapper
    

class RefreshToken:
    @staticmethod
    def check_authorization(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                access_token = request.headers.get('Authorization')
                if not access_token:
                    raise CustomException("리프래쉬 토큰이 제공되지 않았습니다.", 401)
            
                token_info = access_token.split(" ")
                access_token = token_info[1]

                payload = decode_token(access_token, config["SECRET_KEY"])
                return func(auth = payload, *args, **kwargs)
            except jwt.ExpiredSignatureError:
                return custom_response("만료된 리프래쉬 토큰입니다.", code=401)
            except jwt.InvalidTokenError:
                return custom_response("유효하지 않은 리프래쉬 토큰입니다.", code=401)
            except CustomException as e:
                return e.get_response()
            except Exception as e:
                return custom_response("FAIL", code=500)

        return wrapper