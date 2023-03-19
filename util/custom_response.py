from flask import make_response
from util.http_status import get_http_status

def custom_response(message=None, data=None, code=200):
    return make_response({
        "code": get_http_status(code),
        "message": message,
        "data": data
    })
