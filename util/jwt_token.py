import jwt
import os
from flask import make_response, request
from config import config
from functools import wraps

def generate_token(payload, secret):
    return jwt.encode(payload, secret, algorithm="HS256")

def decode_token(payload, secret):
    return jwt.decode(payload, secret, algorithms=["HS256"])
