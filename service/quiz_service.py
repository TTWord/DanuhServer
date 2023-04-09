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
    def generate_multiple_quiz_service(data, db: Database):
        try:
            word_repo = WordRepository(db)

            words = word_repo.find_all_by_book_id(book_id = data['book_id'])

            if len(words) < 4:
                raise CustomException("단어가 4개 미만입니다.", code=400)
            
            if data['number'] > len(words):
                number = len(words)
            else:
                number = data['number']

            word_book = []
            for word in words:
                word_book.append([word['word'], word['mean']])
                 
            random_words = random.sample(word_book, number)

            problem = []

            for _, random_word in enumerate(random_words):
                answer_options = [random_word]
                word_book_copy = [word for word in word_book if word != random_word]
                
                while len(answer_options) < 4:
                    random_meaning = random.choice(word_book_copy)
                    if random_meaning not in answer_options:
                        answer_options.append(random_meaning)

                random.shuffle(answer_options)
                answer_index = answer_options.index(random_word)
                problem.append({"answer_index": answer_index, "answers": answer_options})

            return custom_response("퀴즈 생성 성공", code=200, data={"problem": problem})
        except CustomException as e:
            return e.get_response()
        except Exception as e:
            return custom_response("FAIL", code=500)


    @staticmethod
    @ServiceReceiver.database
    def generate_shortform_quiz_service(data, db: Database):
        try:
            word_repo = WordRepository(db)

            words = word_repo.find_all_by_book_id(book_id = data['book_id'])
            
            if data['number'] > len(words):
                number = len(words)
            else:
                number = data['number']

            random_word = random.sample(words, number)

            problem = []
            for dict in random_word:
                problem.append({"answer": [dict['word'], dict['mean']]})

            return custom_response("데이터 조회 성공", code=200, data={"problem": problem})
        except Exception as e:
            return custom_response("FAIL", code=500)