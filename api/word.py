from flask import Blueprint, request
from services.word import get_word_service

word_route = Blueprint('word', __name__)

@word_route.route('/', methods=['GET'])
def get_word():
    return get_word_service()