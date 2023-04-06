from flask_restx import Namespace, Resource, Api, reqparse, fields
from util.decorator.authorization import Authorization
from flask import request
from service.quiz_service import QuizService


api = Namespace('quiz', description='단어장 API')


quiz_info = api.model('퀴즈 정보', {
    'book_id': fields.Integer(required=True, description='단어장 ID', example=55),
    'number': fields.Integer(required=True, description='풀이 개수', example=10)
})


@api.route("/multiplequiz")
@api.doc(security='Bearer Auth')
class MultipleQuiz(Resource):
    @api.expect(quiz_info)
    @Authorization.reject_authorization
    def post(self):
        """
        객관식 문제 생성
        """
        data = request.get_json()
        return QuizService.generate_multiple_quiz_service(data)
    

@api.route("/shortfromquiz")
@api.doc(security='Bearer Auth')
class ShortFormQuiz(Resource):
    @api.expect(quiz_info)
    @Authorization.reject_authorization
    def post(self):
        """
        주관식 문제 생성
        """
        data = request.get_json()
        return QuizService.generate_shortform_quiz_service(data)