from flask import make_response, request
import jwt
from config import config

class Authorization:
    @staticmethod
    def check_authorization(func):
        def wrapper(*args, **kwargs):
            try:
                access_token = request.headers['Authorization']
            except Exception as e:
                return make_response({"message": "Token not provided"}, 401)
        
            if access_token is not None:
                token_info = access_token.split(" ")
                access_token = token_info[1]
                try:
                    payload = jwt.decode(access_token, config["SECRET_KEY"], "HS256")
                    return func(auth = payload, *args, **kwargs)
                except jwt.InvalidTokenError:
                    return make_response({"message": "Invalid token provided"}, 401)
            else:
                return make_response({"message": "Invalid token provided"}, 401)
        return wrapper
            
    @staticmethod
    def get_authorization(func):
        def wrapper(*args, **kwargs):
            try:
                access_token = request.headers['Authorization']
                
                token_info = access_token.split(" ")
                access_token = token_info[1]
                payload = jwt.decode(access_token, config["SECRET_KEY"], "HS256")
                return func(auth = payload, *args, **kwargs)
            except Exception as e:
                return func(auth = None, *args, **kwargs)
        return wrapper
    
    @staticmethod
    def reject_authorization(func):
        def wrapper(*args, **kwargs):
            try:
                access_token = request.headers['Authorization']
            except Exception as e:
                return make_response({"message": "Token not provided"}, 401)
        
            if access_token is not None:
                token_info = access_token.split(" ")
                access_token = token_info[1]
                try:
                    jwt.decode(access_token, config["SECRET_KEY"], "HS256")
                    return func(*args, **kwargs)
                except jwt.InvalidTokenError:
                    return make_response({"message": "Invalid token provided"}, 401)
            else:
                return make_response({"message": "Invalid token provided"}, 401)
        return wrapper