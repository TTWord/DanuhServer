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
            
            problem = []
            for _ in range(0, data['number']):
                random_word = random.sample(words, 4)

                resultList = []
                for dict in random_word:
                    resultList.append([dict['word'], dict['mean']])

                answer_index = random.randint(0, 3)
                # print(f"{random_word[answer_index]['word']}의 뜻은 무엇인가요?")
                # for i in range(4):
                #     print(f"{i+1}. {resultList[i][1]}")
                # print(f"정답 : {answer_index +1}.{random_word[answer_index]['mean']}")
                data = {"answer_index": answer_index, "answers": resultList}
                problem.append(data)
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

            random_word = random.sample(words, data['number'])

            problem = []
            for dict in random_word:
                problem.append([dict['word'], dict['mean']])
            print(problem)
            return custom_response("데이터 조회 성공", code=200, data={"problem": problem})
        except Exception as e:
            return custom_response("FAIL", code=500)