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

result_info = api.model('결과 정보', {
    'correct': fields.Integer(required=True, description='정답 개수'),
    'count': fields.Integer(required=True, description='단어 개수'),
    'book_ids': fields.String(required=True, description='단어장 아이디(&로 구분)', example='1&2')
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

@api.route("/short")
@api.doc(security='Bearer Auth')
class ShortQuiz(Resource):
    @api.expect(quiz_info)
    @Authorization.check_authorization
    def post(self, auth):
        """
        주관식 문제 생성
        """
        data = request.get_json()
        return QuizService.generate_short_quiz_service(auth=auth, data=data)
    

@api.route("/blind/short")
@api.doc(security='Bearer Auth')
class BlindShortQuiz(Resource):
    @api.expect(quiz_info)
    @Authorization.check_authorization
    def post(self, auth):
        """
        블라인드 주관식 문제 생성
        """
        data = request.get_json()
        return QuizService.generate_blind_short_quiz_service(auth=auth, data=data)


@api.route("/blind/multiple")
@api.doc(security='Bearer Auth')
class BlindMultipleQuiz(Resource):
    @api.expect(quiz_info)
    @Authorization.check_authorization
    def post(self, auth):
        """
        블라인드 주관식 문제 생성
        """
        data = request.get_json()
        return QuizService.generate_blind_multiple_quiz_service(auth=auth, data=data)


@api.route("")
@api.doc(security='Bearer Auth')
class ResultQuiz(Resource):
    @api.expect(result_info)
    @Authorization.check_authorization
    def post(self, auth):
        """
        결과 페이지
        """
        data = request.get_json()
        data['book_ids'] = [int(book_id) for book_id in data['book_ids'].split("&")]
        return QuizService.get_result_service(auth=auth, data=data)
    