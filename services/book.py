from flask import jsonify

def get_book_service():
    # get book from database
    book = [
      {
        "id": 1,
        "name": "책",
      }
    ]
    
    return jsonify(book)