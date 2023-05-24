from flask_restx import Namespace, Resource, Api, reqparse, fields
from util.decorator.authorization import Authorization
from flask import request
from service.quiz_service import QuizService


api = Namespace('quiz', description='퀴즈 API')
quiz_info = api.model('퀴즈 정보', {
    'book_ids': fields.String(required=True, description='단어장 ID', example="19&21"),
    'count': fields.Integer(required=True, description='풀이 개수', example=10),
    # 암기 여부에 따른 필터링
    'memorized_filter': fields.Boolean(required=False, description='암기 필터링', example=False)
})

@api.route("/multiple")
@api.doc(security='Bearer Auth')
class MultipleQuiz(Resource):
    @api.expect(quiz_info)
    @Authorization.check_authorization
    def post(self, auth):
        """
        객관식 문제 생성
        """
        data = request.get_json()

        return QuizService.generate_multiple_quiz_service(auth=auth, data=data)

@api.route("/shortform")
@api.doc(security='Bearer Auth')
class ShortFormQuiz(Resource):
    @api.expect(quiz_info)
    @Authorization.check_authorization
    def post(self, auth):
        """
        주관식 문제 생성
        """
        data = request.get_json()
        return QuizService.generate_shortform_quiz_service(auth=auth, data=data)