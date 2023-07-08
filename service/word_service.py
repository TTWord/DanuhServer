from util.custom_response import custom_response
from util.decorator.service_receiver import ServiceReceiver
from util.exception import CustomException
from db.connect import Database
from repository.word_repository import WordRepository
from repository.book_repository import BookRepository
from repository.share_repository import ShareRepository
from util.validation import validate_word


class WordService:
    @staticmethod
    @ServiceReceiver.database
    def get_words_by_book_id(book_id, auth, db: Database):
        try:
            book_repo = BookRepository(db)
            book = book_repo.find_one_by_id(book_id)
            if not book:
                raise CustomException("단어장이 존재하지 않습니다.", code=409)
            elif book["user_id"] != auth["id"]:
                raise CustomException("단어장 조회 권한이 없습니다.", code=403)
            
            words = WordRepository(db).find_all_by_book_id(book_id)
            return custom_response("SUCCESS", data=words)
        except CustomException as e:
            return e.get_response()
        except Exception as e:
            return custom_response("FAIL", code=500)
    
    @staticmethod
    @ServiceReceiver.database
    def get_word_by_id(id, db: Database):
        try:
            word = WordRepository(db).find_one_by_id(id)
            if word is None:
                raise CustomException("단어장이 존재하지 않습니다.", code=409)
            return custom_response("SUCCESS", data=word)
        except CustomException as e:
            return e.get_response()
        except Exception as e:
            return custom_response("FAIL", code=500)
    
    @staticmethod
    @ServiceReceiver.database
    def add(book_id, data, auth, db: Database):
        try:
            if not validate_word(data['word'], data['mean']):
                raise CustomException("단어나 의미가 15자를 초과합니다.", code=400)
            
            word_repo = WordRepository(db)
            book_repo = BookRepository(db)
            share_repo = ShareRepository(db)

            book = book_repo.find_one_by_id(book_id)
            if not book:
                raise CustomException("단어장이 존재하지 않습니다.", code=409)
            elif book["user_id"] != auth["id"]:
                raise CustomException("단어장 조회 권한이 없습니다.", code=409)
            
            # 다운로드 받은 단어장에 대한 예외 적용
            share = share_repo.find_one_by_id(book['share_id'])
            if share and book["id"] != share["book_id"]:
                raise CustomException("다운로드 받은 단어장에 대해서 단어를 추가할 수 없습니다.", code=409)
            
            words = word_repo.find_all_by_book_id(book_id=book['id'])
            for word in words:
                if word['word'] == data['word'] and word['mean'] == data['mean']:
                    raise CustomException("이미 존재하는 단어입니다.", code=409)
            
            word = word_repo.add(book_id= book_id, word=data["word"], mean=data["mean"])
            return custom_response("SUCCESS", data=word)
        except CustomException as e:
            return e.get_response()
        except Exception as e:
            print(e)
            return custom_response("FAIL", code=500)
        
    @staticmethod
    @ServiceReceiver.database
    def update(id, data, auth, db: Database):
        try:
            if not validate_word(data['word'], data['mean']):
                raise CustomException("단어나 의미가 15자를 초과합니다.", code=400)
            
            word_repo = WordRepository(db)
            # 데이터 중복 검사
            word = word_repo.find_one_by_id(id=id)
            if not word:
                raise CustomException("존재하지 않는 단어입니다.", code=409)
            
            # user_id와 검사
            user_info = BookRepository(db).find_one_by_id(word['book_id'])
            if user_info['user_id'] != auth['id']:
                raise CustomException("단어장 조회 권한이 없습니다.", code=403)

            word = word_repo.update(id=id, book_id=word['book_id'], word=data["word"], mean=data["mean"])
            return custom_response("SUCCESS", data=word)
        except CustomException as e:
            return e.get_response()
        except Exception as e:
            return custom_response("FAIL", code=500)
    
    @staticmethod
    @ServiceReceiver.database
    def delete(id, auth, db: Database):
        try:
            word_repo = WordRepository(db)

            # 데이터 중복 검사
            word = word_repo.find_one_by_id(id)
            if not word:
                raise CustomException("단어가 존재하지 않습니다.", code=404)
            
            # user_id와 검사
            user_info = BookRepository(db).find_one_by_id(word['book_id'])
            if user_info['user_id'] != auth['id']:
                raise CustomException("단어 조회 권한이 없습니다.", code=403)

            word = word_repo.delete(id=id)
            return custom_response("SUCCESS", data=word)
        except CustomException as e:
            return e.get_response()
        except Exception as e:
            return custom_response("FAIL", code=500)
