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
                raise CustomException("BOOK_NOT_FOUND", code=409)
            elif book["user_id"] != auth["id"]:
                raise CustomException("BOOK_ACCESS_DENIED", code=403)
            
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
                raise CustomException("BOOK_NOT_FOUND", code=409)
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
                raise CustomException("WORD_COUNT_MORE_THAN_LIMIT", code=400)
            
            word_repo = WordRepository(db)
            book_repo = BookRepository(db)
            share_repo = ShareRepository(db)

            word_len = 0
            books = book_repo.find_all_by_user_id(auth['id'])
            for book in books:
                word_len += len(word_repo.find_all_by_book_id(book['id']))

            if word_len > 200:
                raise CustomException("WORD_MORE_THAN_LIMIT", code=409)

            book = book_repo.find_one_by_id(book_id)
            if not book:
                raise CustomException("BOOK_NOT_FOUND", code=409)
            elif book["user_id"] != auth["id"]:
                raise CustomException("BOOK_ACCESS_DENIED", code=409)
            
            # 다운로드 받은 단어장에 대한 예외 적용
            if book['is_downloaded']:
                raise CustomException("BOOK_DOWNLOADED", code=409)
            
            words = word_repo.find_all_by_book_id(book_id=book['id'])
            for word in words:
                if word['word'] == data['word'] and word['mean'] == data['mean']:
                    raise CustomException("WORD_ALREADY_EXIST", code=409)
            
            word = word_repo.add(book_id=book_id, word=data["word"], mean=data["mean"])
            
            # 단어 추가가 완료되었다면 word_count 추가
            if word is not None:
                book_repo.patch_book_word_count(id=book["id"], count=(book["word_count"] + 1))
            
            return custom_response("SUCCESS", data=word)
        except CustomException as e:
            return e.get_response()
        except Exception as e:
            return custom_response("FAIL", code=500)
        
    @staticmethod
    @ServiceReceiver.database
    def update(id, data, auth, db: Database):
        try:
            if not validate_word(data['word'], data['mean']):
                raise CustomException("WORD_COUNT_MORE_THAN_LIMIT", code=400)
            
            word_repo = WordRepository(db)
            book_repo = BookRepository(db)

            # 데이터 중복 검사
            word = word_repo.find_one_by_id(id=id)
            book = book_repo.find_one_by_id(word['book_id'])

            if book['is_downloaded']:
                raise CustomException("BOOK_IS_DOWNLOADED", code=409)

            if not word:
                raise CustomException("WORD_NOT_FOUND", code=409)
            
            # user_id와 검사
            user_info = BookRepository(db).find_one_by_id(word['book_id'])
            if user_info['user_id'] != auth['id']:
                raise CustomException("BOOK_ACCESS_DENIED", code=403)

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
            book_repo = BookRepository(db)

            # 데이터 중복 검사
            word = word_repo.find_one_by_id(id)
            if not word:
                raise CustomException("WORD_NOT_FOUND", code=404)
            
            # user_id와 검사
            book = BookRepository(db).find_one_by_id(word['book_id'])
            if book['is_downloaded']:
                raise CustomException("BOOK_IS_DOWNLOADED", code=409)
            if book['user_id'] != auth['id']:
                raise CustomException("BOOK_ACCESS_DENIED", code=403)
            
            book_id = word["book_id"]

            word = word_repo.delete(id=id)
            
            # 단어 삭제가 성공했다면 북 카운트 감소
            if word is not None:
                book = book_repo.find_one_by_id(book_id)
                
                book_repo.patch_book_word_count(id=book["id"], count=(book["word_count"] - 1))
            
            return custom_response("SUCCESS", data=word)
        except CustomException as e:
            return e.get_response()
        except Exception as e:
            return custom_response("FAIL", code=500)
