from util.decorator.service_receiver import ServiceReceiver
from util.custom_response import custom_response
from util.exception import CustomException
from db.connect import Database
from repository.book_repository import BookRepository
from repository.word_repository import WordRepository
import random


class QuizService:
    @staticmethod
    @ServiceReceiver.database
    def generate_multiple_quiz_service(data, auth, db: Database):
        try:
            book_repo = BookRepository(db)
            
            book = book_repo.find_one_by_id(id = data['book_id'])
            
            if book is None:
                raise CustomException("BOOK_NOT_FOUND", code=409)
            
            if book['user_id'] != auth['id']:
                raise CustomException("BOOK_ACCESS_DENIED", code=403)
            
            word_repo = WordRepository(db)

            words = word_repo.find_all_by_book_id(book_id = data['book_id'])

            if len(words) < 4:
                raise CustomException("WORD_LESS_THAN_COUNT", code=400) # 단어가 4개 미만인 경우
            
            if data['number'] > len(words):
                number = len(words)
            else:
                number = data['number']
                 
            random_words = random.sample(words, number)

            problem = []

            for _, random_word in enumerate(random_words):
                answer_options = [[random_word['word'], random_word['mean']]]
                word_book_copy = [word for word in words if word != random_word]

                while len(answer_options) < 4:
                    random_meaning = random.choice(word_book_copy)
                    random_meaning = [random_meaning['word'], random_meaning['mean']]

                    if random_meaning not in answer_options:
                        answer_options.append(random_meaning)

                random.shuffle(answer_options)
                answer_index = answer_options.index([random_word['word'], random_word['mean']])
                problem.append({"answer_index": answer_index, "answers": answer_options, "word_id": random_word['id']})

            return custom_response("SUCCESS", code=200, data={"problem": problem})
        except CustomException as e:
            return e.get_response()
        except Exception as e:
            return custom_response("FAIL", code=500)


    @staticmethod
    @ServiceReceiver.database
    def generate_shortform_quiz_service(data, auth, db: Database):
        try:
            book_repo = BookRepository(db)
            
            book = book_repo.find_one_by_id(id = data['book_id'])
            
            if book is None:
                raise CustomException("BOOK_NOT_FOUND", code=409)
            
            if book['user_id'] != auth['id']:
                raise CustomException("BOOK_ACCESS_DENIED", code=403)
            
            word_repo = WordRepository(db)

            words = word_repo.find_all_by_book_id(book_id = data['book_id'])
            
            if data['number'] > len(words):
                number = len(words)
            else:
                number = data['number']

            random_word = random.sample(words, number)

            problem = []
            for dict in random_word:
                problem.append({"answer": [dict['word'], dict['mean']], "word_id": dict['id']})

            return custom_response("SUCCESS", code=200, data={"problem": problem})
        except Exception as e:
            return custom_response("FAIL", code=500)