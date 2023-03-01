from flask import jsonify
from repository.book_repository import BookRepository
from db.connect import Database

class BookService:
    @staticmethod
    def get_books_all():
        db = Database()
        db.connect()
        
        books = BookRepository(db).find_all()
        
        db.disconnect()
        
        return jsonify(books)
    
    @staticmethod
    def get_book_by_id(id):
        db = Database()
        
        book = BookRepository(db).find_by_id(id)
        
        return jsonify(book)
