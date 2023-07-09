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
    def generate_memo_service(db: Database, auth, data):
        try:
            book_repo = BookRepository(db)

            word_book = []

            for book_id in data['book_ids']:
                book = book_repo.find_one_by_id(id = book_id)
            
                if book is None:
                    raise CustomException("BOOK_NOT_FOUND", code=409)
                
                if book['user_id'] != auth['id']:
                    raise CustomException("BOOK_ACCESS_DENIED", code=403)
                
                word_repo = WordRepository(db)

                words = word_repo.find_all_by_book_id(book_id = book_id)

                for word in words:
                    word_book.append({"word": word['word'], "mean": word['mean'], 
                                      "is_memorized": word['is_memorized']})
            if len(word_book) < 4:
                raise CustomException("WORD_LESS_THAN_COUNT", code=400)
            
            if data['count'] > len(word_book):
                number = len(word_book)
            else:
                number = data['count']    

            random_words = random.sample(word_book, number)
            
            return custom_response("SUCCESS", code=200, data={"words": random_words})
        except CustomException as e:
            return e.get_response()
        except Exception as e:
            return custom_response("FAIL", code=500)
        
    @staticmethod
    @ServiceReceiver.database
    def update_memo_service(db: Database, data):
        try:
            word_repo = WordRepository(db)

            word = word_repo.find_one_by_id(id = data['word_id'])
            if not word:
                raise CustomException("WORD_NOT_FOUND", code=409)
            
            data = word_repo.update_memorized(id = data['word_id'], is_memorized = data['is_memorized'])

            return custom_response("SUCCESS", code=200, data=data)
        except CustomException as e:
            return e.get_response()
        except Exception as e:
            return custom_response("FAIL", code=500)
        
    @staticmethod
    @ServiceReceiver.database
    def get_result_service(db: Database, auth, data):
        try:
            words = []
            word_repo = WordRepository(db)
            book_repo = BookRepository(db)

            books = book_repo.find_all_by_user_id(auth['id'])
            if len(books) == len(data['book_ids']):
                books = "전체"
            else:
                books = ','.join(str(s) for s in data['book_ids'])

            for book_id in data['book_ids']:
                words.extend(word_repo.find_all_by_book_id(book_id))

            memorized_word = [i for i in words if i['is_memorized']]

            data = {'books': books, 'total_count': len(words), 'memorized_count': len(memorized_word),
                    'count': data['count'], 'correct_prob': str(int(data['correct']/data['count']*100)) + "%"}
            return custom_response("SUCCESS", code=200, data=data)
        except CustomException as e:
            return e.get_response()
        except Exception as e:
            print(e)
            return custom_response("FAIL", code=500)