from flask import make_response
from util.http_status import get_http_status

class CustomException(Exception):
    def __init__(self, message, code=400, data=None):
        super(CustomException, self).__init__(message)
        self.message = message
        self.code = code
        self.data = data


    def get_response(self):
        return make_response({
            "status": get_http_status(self.code),
            "message": self.message,
            "data": self.data
        })
