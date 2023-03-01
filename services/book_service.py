from flask import jsonify
from model.book import BookModel

class BookService:
    @staticmethod
    def get_books_all():
        books = BookModel().find_all()
        
        return jsonify(books)
    
    @staticmethod
    def get_book_by_id(id):
        book = BookModel().find_by_id(id)
        
        return jsonify(book)
