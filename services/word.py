from flask import jsonify

def get_word_service():
    # get word from database
    word = [
      {
        "id": 1,
        "name": "hello",
      }
    ]
    
    return jsonify(word)