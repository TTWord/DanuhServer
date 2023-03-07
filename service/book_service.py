from flask import jsonify, make_response
from repository.book_repository import BookRepository
from db.connect import Database

    
class Response:
    def __init__(self, func):
        self.func = func
        
    def __call__(self, *args, **kwargs):
        db = Database()
        db.connect()
        
        data = self.func(db = db, *args, **kwargs)
        
        db.disconnect()
        
        return make_response(data['data'], data['code'])


class BookService:
    @staticmethod
    @Response
    def get_books_all(db):
        books = BookRepository(db).find_all()
        
        return { "code" : 200, "data" : books }
    
    @staticmethod
    def get_books_by_user_id(user_id: int):
        db = Database()
        db.connect()
        
        db.disconnect()
        
        return { "code": 200, "data": "get_books_by_user_id" }
    
    @staticmethod
    def get_book_by_id(id):
        db = Database()
        
        book = BookRepository(db).find_by_id(id)
        
        return { "code": 200, "data": book }
