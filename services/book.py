from flask import jsonify
from model.book import Book
import json

def get_book_service():
    books = Book.get_books()
    
    return jsonify(books)