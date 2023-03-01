from services.word_service import get_word_service
from flask_restx import Namespace, Resource, Api


api = Namespace('words', description='Book related operations')

@api.route('')
class Word(Resource):
    @api.doc('user_word')
    def get(self):
        return get_word_service()
    