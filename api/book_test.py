from service.book_service import BookService
from flask_restx import Namespace, Resource, Api, reqparse, fields
from util.decorator.authorization import Authorization


api = Namespace('book_test', description='단어장 API')

input_text = api.model('예측', {
    'text': fields.String(required=True, description='예측 값 입력', example='You can tell a stranger that this is shiitake mushrooms.')
})



# TODO : Refactoring 필요
import requests
import json
from flask import request
from config import config
@api.route('/predict')
class Booktest(Resource):
    @api.expect(input_text, validate=True)
    def post(self):
        url = f"{config['AI_IP']}"
        input_data = request.get_json()
        response = requests.post(url, json=input_data)
        result = json.loads(response.content)

        # Print the result
        return result
    
    