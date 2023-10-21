from flask_restx import Namespace, Resource, Api, reqparse, fields
from util.decorator.authorization import Authorization
from flask import request
from service.quiz_service import QuizService
import json

api = Namespace('quiz', description='퀴즈 API')
quiz_info = api.model('퀴즈 정보', {
    'book_ids': fields.String(required=True, description='단어장 ID', example="19&21"),
    'count': fields.Integer(required=True, description='풀이 개수', example=10),
    # 암기 여부에 따른 필터링
    'memorized_filter': fields.Boolean(required=False, description='암기 필터링', example=False)
})

blind_quiz_info = api.model('객관식 블라인드 퀴즈 정보', {
    **quiz_info,
    'choice_count': fields.Integer(required=False, description='선택지 개수', example=4)
})

result_info = api.model('결과 정보', {
    'correct': fields.Integer(required=True, description='정답 개수'),
    'count': fields.Integer(required=True, description='단어 개수'),
    'book_ids': fields.String(required=True, description='단어장 아이디(&로 구분)', example='1&2')
})


# TODO : model 정리 필요
#       - 부가적인 정보에 따라서 많은 모델을 생성해야함
@api.route("/multiple")
@api.doc(security='Bearer Auth')
class MultipleQuiz(Resource):
    @api.response(200, "SUCCESS")
    @api.response(400, "WORD_LESS_THAN_COUNT")
    @api.response(403, "BOOK_IDS_NOT_INSERTED, BOOK_ACCESS_DENIED")
    @api.response(409, "BOOK_NOT_FOUND")
    @api.response(500, "FAIL")
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
    @api.response(200, "SUCCESS")
    @api.response(403, "BOOK_IDS_NOT_INSERTED, BOOK_ACCESS_DENIED")
    @api.response(409, "BOOK_NOT_FOUND")
    @api.response(500, "FAIL")
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
    @api.response(200, "SUCCESS")
    @api.response(403, "BOOK_IDS_NOT_INSERTED, BOOK_ACCESS_DENIED")
    @api.response(409, "BOOK_NOT_FOUND")
    @api.response(500, "FAIL")
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
    @api.response(200, "SUCCESS")
    @api.response(400, "WORD_LESS_THAN_COUNT")
    @api.response(403, "BOOK_IDS_NOT_INSERTED, BOOK_ACCESS_DENIED")
    @api.response(409, "BOOK_NOT_FOUND, QUIZ_COUNT_ERROR")
    @api.response(500, "FAIL")
    @api.expect(blind_quiz_info)
    @Authorization.check_authorization
    def post(self, auth):
        """
        블라인드 객관식 문제 생성
        """
        data = request.get_json()
        return QuizService.generate_blind_multiple_quiz_service(auth=auth, data=data)


@api.route("")
@api.doc(security='Bearer Auth')
class ResultQuiz(Resource):
    @api.response(200, "SUCCESS")
    @api.response(403, "BOOK_IDS_NOT_INSERTED")
    @api.response(500, "FAIL")
    @api.expect(result_info)
    @Authorization.check_authorization
    def post(self, auth):
        """
        결과 페이지
        """
        data = request.get_json()
        data['book_ids'] = [int(book_id) for book_id in data['book_ids'].split("&")]
        return QuizService.get_result_service(auth=auth, data=data)
    
    

@api.route('/recommend')
@api.doc(security="Bearer Auth")
class BookRecommend(Resource):
    @api.response(200, "SUCCESS")
    @api.doc(params={'books': (
                     "배열 안에 book_id 리스트\r\n"
                     "ex ) recommend?books=[1,2,3,4]\r\n"
                     "만약 전체인 경우 books=[]로 요청\r\n"
                     )})
    @Authorization.check_authorization
    def get(self, auth):
        """
        책 목록 받아서 최초 조회 여부에 따라 추천 북 목록 주는 API
        """
        books = json.loads(request.args.get('books'))
        
        return QuizService.get_quiz_start_view_books(auth, data={
            "books": books
        })