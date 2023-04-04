from flask_restx import Namespace, Resource, Api, reqparse, fields
from util.decorator.authorization import Authorization
from flask import request
from service.quiz_service import QuizService


api = Namespace('memo', description='단어장 API')

@api.route("")
@api.doc(security='Bearer Auth')
class Memo(Resource):
    @Authorization.check_authorization
    def get(self, auth):
        """
        단어 암기
        """
        return QuizService.quiz_service(auth)