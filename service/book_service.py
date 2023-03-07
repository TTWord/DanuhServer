from flask import jsonify, make_response
from repository.book_repository import BookRepository
from db.connect import Database
from repository.user_repository import UserRepository
from util.http_status import get_http_status
from util.exception import CustomException

def response(func):
    def wrapper(*args, **kwargs):
        db = Database()
        db.connect()
        
        data = func(db = db, *args, **kwargs)
        
        db.disconnect()
        
        return make_response({
            "status": get_http_status(data['code']),
            "comment": data['comment'],
            "data": data['data']
        }, data['code'])
        
    return wrapper

class BookService:
    @staticmethod
    @response
    def get_books_all(db):
        books = BookRepository(db).find_all()
        
        return { "code" : 200, "data" : books }
    
    @staticmethod
    @response
    def get_books_by_user_id(auth, db: Database):
        try:        
            books = BookRepository(db).find_all_by_user_id(user_id = auth['id'])
        except:
            return { "code": 400, "data": None, "comment": "단어장 목록 조회 실패" }
        
        return { "code": 200, "data": books, "comment": "데이터 조회 성공" }
    
    @staticmethod
    @response
    def get_book_by_id(id, db: Database):
        try:
            book = BookRepository(db).find_one_by_id(id)
        except:
            return { "code": 400, "data": None, "comment": "단어장 조회 실패" }
        
        return { "code": 200, "data": book, "comment": "데이터 조회 성공" }
    
    @staticmethod
    @response
    def add_book(auth, data, db: Database):
        try:
            if data["name"] is None:
                raise CustomException("None")
            
            # 데이터 중복 검사
            book = BookRepository(db).find_one_by_name_and_user_id(name = data["name"], user_id = auth['id'])
            
            if book is not None:
                raise CustomException("Overlap")
            
            book = BookRepository(db).add(user_id = auth['id'], name = data["name"])
            
            return { "code": 200, "data": book, "comment": "데이터 추가 성공" }
        except CustomException as e:
            error = e.args[0]
            if error == "None":
                return { "code": 400, "data": None, "comment": "데이터에 단어장 이름이 없습니다" }
            if error == "Overlap":
                return { "code": 400, "data": None, "comment": "단어장 이름이 중복입니다" }
        except:
            return { "code": 500, "data": None, "comment": "단어장 추가 실패" }
