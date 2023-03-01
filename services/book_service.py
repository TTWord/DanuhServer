from flask import jsonify
from model.book import BookModel
from db.connect import Database

class BookService:
    @staticmethod
    def get_books_all():
        db = Database()
        db.connect()
        
        books = BookModel(db).find_all()
        
        db.disconnect()
        
        return jsonify(books)
    
    @staticmethod
    def get_book_by_id(id):
        db = Database()
        
        book = BookModel(db).find_by_id(id)
        
        return jsonify(book)
