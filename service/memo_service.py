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
    def generate_flash_memo_service(db: Database, auth, data):
        try:
            if "book_ids" not in data.keys():
                raise CustomException("BOOK_IDS_NOT_INSERTED", code=403)
            elif "count" not in data.keys():
                data['count'] = 10

            data['book_ids'] = [int(book_id) for book_id in data['book_ids'].split("&")]

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
    def generate_blind_memo_service(data, auth, db: Database):
        try:
            if "book_ids" not in data.keys():
                raise CustomException("BOOK_IDS_NOT_INSERTED", code=403)
            elif "count" not in data.keys():
                data['count'] = 10

            book_repo = BookRepository(db)
            word_repo = WordRepository(db)

            book_ids = [int(book_id) for book_id in data['book_ids'].split("&")]
            all_words = []
            for book_id in book_ids:
                book = book_repo.find_one_by_id(id = book_id)
                if book is None:
                    raise CustomException("BOOK_NOT_FOUND", code=409)
                
                if book['user_id'] != auth['id']:
                    raise CustomException("BOOK_ACCESS_DENIED", code=403)
                words = word_repo.find_all_by_book_id(book_id = book_id)
                all_words.extend(words)

            if data['count'] > len(all_words):
                number = len(all_words)
            else:
                number = data['count']

            random_word = random.sample(all_words, number)

            problem = []
            for dict in random_word:
                problem.append({'word': dict['word'], 'mean': dict['mean'], 
                                "is_memorized": dict['is_memorized']})

            return custom_response("SUCCESS", code=200, data={"words": problem})
        except CustomException as e:
            return e.get_response()
        except Exception as e:
            return custom_response("FAIL", code=500)