from util.decorator.service_receiver import ServiceReceiver
from db.connect import Database
from util.custom_response import custom_response
from repository.word_repository import WordRepository
from repository.book_repository import BookRepository
from util.exception import CustomException
import random


class MemoService:
    @staticmethod
    @ServiceReceiver.database
    def memo_service(db: Database, auth, data):
        try:
            book_repo = BookRepository(db)
            
            book = book_repo.find_one_by_id(id = data['book_id'])
            
            if book is None:
                raise CustomException("BOOK_NOT_FOUND", code=409)
            
            if book['user_id'] != auth['id']:
                raise CustomException("BOOK_ACCESS_DENIED", code=403)
            
            word_repo = WordRepository(db)

            words = word_repo.find_all_by_book_id(book_id = data['book_id'])

            if len(words) < 4:
                raise CustomException("WORD_LESS_THAN_COUNT", code=400)
            
            if data['count'] > len(words):
                number = len(words)
            else:
                number = data['count']

            word_book = []
            for word in words:
                word_book.append({"word": word['word'], "mean": word['mean']})
                 
            random_words = random.sample(word_book, number)
            
            return custom_response("SUCCESS", code=200, data={"words": random_words})
        except CustomException as e:
            return e.get_response()
        except Exception as e:
            return custom_response("FAIL", code=500)