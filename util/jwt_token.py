import jwt
import os
from flask import make_response, request
from config import config
from functools import wraps

def generate_token(payload, secret):
    return jwt.encode(payload, secret, algorithm="HS256")

def decode_token(payload, secret):
    return jwt.decode(payload, secret, algorithms=["HS256"])

# TODO: 데코레이터 학습
def validate_token(func):
    secret = config['SECRET_KEY']
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(args)
        try:
            access_token = request.headers['Authorization']
        except Exception as e:
            return make_response({"message": "Token not provided"}, 403)
        
        if access_token is not None:
            token_info = access_token.split(" ")
            access_token = token_info[1]
            try:
                payload = jwt.decode(access_token, secret, "HS256")
                return make_response({**payload, "message": "Login Success"}, 200)
            except jwt.InvalidTokenError:
                payload = None
            if payload is None:
                return make_response({"message": "Invalid token provided"}, 403)

        else:
            return make_response({"message": "Invalid token provided"}, 403)

        return func(*args, **kwargs)
    return wrapper