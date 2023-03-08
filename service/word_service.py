from flask import jsonify, make_response
from db.connect import Database
from repository.word_repository import WordRepository


class WordService:
    @staticmethod
    def get_words_by_book_id(data):
        try:
            db = Database()
            with db.connect():
                words = WordRepository(db).find_all_by_book_id(1)
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
    def update(id, data):
        try:
            db = Database()
            with db.connect():
                # 데이터 중복 검사
                word = WordRepository(db).find_one_by_id(id =data['id'])
                if word:
                    return make_response({'message': 'word not in book'}, 401)
                word = WordRepository(db).update(id=id, word=data["word"], mean=data["mean"])
            return make_response({'message': 'Succesfully updated',
                                  "data": word}, 200)
        except Exception as e:
            return make_response({'message': str(e)}, 404)
    
    @staticmethod
    def delete(id):
        try:
            db = Database()
            with db.connect():
                # 데이터 중복 검사
                word = WordRepository(db).find_one_by_id(id)
                if not word:
                    return make_response({'message': str(e)}, 404)
                word = WordRepository(db).delete(id=id)
        except Exception as e:
            return make_response({'message': str(e)}, 404)
