from flask import jsonify, make_response
from db.connect import Database
from repository.word_repository import WordRepository
from repository.book_repository import BookRepository


# TODO 글자수 제한 추가(원문 15자, 번역 15자)
class WordService:
    @staticmethod
    def get_words_by_book_id(data):
        try:
            db = Database()
            with db.connect():
                words = WordRepository(db).find_all_by_book_id(data['book_id'])
            return make_response({'message': 'Succesfully inserted',
                                  "data": words}, 200)
        except Exception as e:
            return make_response({'message': str(e)}, 404)
    
    @staticmethod
    def get_word_by_id(id):
        try:
            db = Database()
            with db.connect():
                word = WordRepository(db).find_one_by_id(id)
            return make_response({'message': 'Succesfully inserted',
                                  "data": word}, 200)
        except Exception as e:
            return make_response({'message': str(e)}, 404)
    
    @staticmethod
    def add(data):
        try:
            db = Database()
            with db.connect():
                # 데이터 중복 검사
                # word = WordRepository(db).find_one_by_name_and_user_id(name = data["name"], user_id = auth['id'])
                word = WordRepository(db).add(book_id= data['book_id'], word=data["word"], mean=data["mean"])
            return make_response({'message': 'Succesfully inserted',
                                  "data": word}, 200)
        except Exception as e:
            return make_response({'message': str(e)}, 404)
        
    @staticmethod
    def update(id, data, auth):
        try:
            db = Database()
            with db.connect():
                # 데이터 중복 검사
                word = WordRepository(db).find_one_by_id(id=id)

                # user_id와 검사
                user_info = BookRepository(db).find_one_by_id(word['book_id'])
                if user_info['user_id'] != auth['id']:
                    return make_response({'message': 'user_id not match'}, 403)
                
                if not word:
                    return make_response({'message': 'word not in book'}, 403)

                word = WordRepository(db).update(id=id, book_id=data["book_id"], word=data["word"], mean=data["mean"])
            return make_response({'message': 'Succesfully updated',
                                  "data": word}, 200)
        except Exception as e:
            return make_response({'message': str(e)}, 404)
    
    @staticmethod
    def delete(id, auth):
        try:
            db = Database()
            with db.connect():
                # 데이터 중복 검사
                word = WordRepository(db).find_one_by_id(id)

                # user_id와 검사
                user_info = BookRepository(db).find_one_by_id(word['book_id'])
                if user_info['user_id'] != auth['id']:
                    return make_response({'message': 'user_id not match'}, 403)

                if not word:
                    return make_response({'message': str(e)}, 404)
                word = WordRepository(db).delete(id=id)
                return make_response({'message': 'Succesfully Deleted'}, 200)
        except Exception as e:
            return make_response({'message': str(e)}, 404)
