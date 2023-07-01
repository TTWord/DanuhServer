from repository.book_repository import BookRepository
from repository.word_repository import WordRepository
from repository.share_repository import ShareRepository
from db.connect import Database
from util.custom_response import custom_response
from util.decorator.service_receiver import ServiceReceiver
from util.exception import CustomException
from config import config
import requests
import json
from collections import defaultdict 


class BookService:
    @staticmethod
    @ServiceReceiver.database
    def get_books_all(db):
        books = BookRepository(db).find_all()
        
        return { "code" : 200, "data" : books }
    
    @staticmethod
    @ServiceReceiver.database
    def get_books_by_user_id(auth, db: Database):
        try:
            books = BookRepository(db).find_all_by_user_id(user_id = auth['id'])
            return custom_response("데이터 조회 성공", data=books,)
        except:
            return custom_response("단어장 목록 조회 실패", code=500)
    
    @staticmethod
    @ServiceReceiver.database
    def get_book_by_id(auth, id, db: Database):
        try:
            book = BookRepository(db).find_one_by_id(id)
            
            if book is None:
                raise CustomException("단어장이 존재하지 않습니다.", code=404)
            
            if book["user_id"] != auth["id"]:
                raise CustomException("단어장 조회 권한이 없습니다.", code=403)
            
            return custom_response("데이터 조회 성공", code=200, data=book)
        except CustomException as e:
            return e.get_response()
        except Exception as e:
            return custom_response("단어장 조회 실패", code=500)
    
    @staticmethod
    @ServiceReceiver.database
    def add_book(auth, data, db: Database):
        try:
            if data["name"] is None:
                raise CustomException("데이터에 단어장 이름이 없습니다.")
            
            book_repo = BookRepository(db)
            
            # 데이터 중복 검사
            book = book_repo.find_one_by_name_and_user_id(name = data["name"], user_id = auth['id'])
            
            if book is not None:
                raise CustomException("단어장 이름이 중복입니다.", code=409)
            
            book = book_repo.add(user_id = auth['id'], name = data["name"])
            
            return custom_response("데이터 추가 성공", data=book)
        except CustomException as e:
            return e.get_response()
        except:
            return custom_response("단어장 추가 실패", code=500)
        
    @staticmethod
    @ServiceReceiver.database
    def generate_book(auth, data, db: Database):
        try:
            url = f"{config['AI_IP']}"
            response = requests.post(url, json=data)
            result = json.loads(response.content)
            if data["name"] is None:
                raise CustomException("데이터에 단어장 이름이 없습니다.")

            book_repo = BookRepository(db)
            
            # 데이터 중복 검사
            book = book_repo.find_one_by_name_and_user_id(name = data["name"], user_id = auth['id'])
            
            if book is not None:
                raise CustomException("단어장 이름이 중복입니다.", code=409)
            
            book_info = book_repo.add(user_id = auth['id'], name = data["name"])

            book_id = book_info["id"]
            word_repo = WordRepository(db)

            dict_check = defaultdict(str)
            for word, mean in result['words'].items():
                if word not in dict_check.keys() and mean != dict_check[word]:
                    dict_check[word] = mean
 
            for word, mean in result['words'].items():
                word_repo.add(book_id, word, mean)

            return custom_response("데이터 추가 성공", data=book_info)
        except CustomException as e:
            return e.get_response()
        except Exception as e:
            return custom_response("단어장 추가 실패", code=500)
        
    @staticmethod
    @ServiceReceiver.database
    def update_book(auth, id, data, db: Database):
        try:
            if data["name"] is None:
                raise CustomException("전송한 데이터에 변경할 단어장 이름이 없습니다.")
            
            book_repo = BookRepository(db)
            
            # 변경할 데이터가 있는지 조회
            book = book_repo.find_one_by_id(id = id)
            
            # 데이터가 없을 경우
            if book is None:
                raise CustomException("단어장이 존재하지 않습니다.", code=404)
            
            # 같은 유저에 같은 이름을 가진 단어장이 있는지 체크
            same_book = book_repo.find_one_by_name_and_user_id(name = data["name"], user_id = auth['id'])
            
            # 중복 체크
            if same_book is not None:
                raise CustomException("단어장 이름이 중복입니다.", code=409)
            
            # 유저 ID 검사
            if book["user_id"] != auth["id"]:
                raise CustomException("단어장 변경 권한이 없습니다.", code=403)
            
            book = book_repo.update(id = id, name = data["name"])
            
            return custom_response("단어장 수정 성공", data=book)
        except CustomException as e:
            return e.get_response()
        except:
            return custom_response("단어장 수정 실패", code=500)
            
    @staticmethod
    @ServiceReceiver.database
    def update_share_book(auth, id, db: Database):
        try:
            book_repo = BookRepository(db)
            share_repo = ShareRepository(db)
            word_repo = WordRepository(db)

            # 변경할 데이터가 있는지 조회
            book = book_repo.find_one_by_id(id = id)

            if auth['id'] != book['user_id']:
                raise CustomException("단어장 변경 권한이 없습니다.", code=403)
            # 데이터가 없을 경우
            if book is None:
                raise CustomException("단어장이 존재하지 않습니다.", code=404)
            
            share = share_repo.find_one_by_id(book['share_id'])
            if share is None:
                raise CustomException("다운로드 받은 단어장이 아닙니다.", code=409)
            
            # 다운로드 증가
            share_repo.update_column(share['id'], 'downloaded')

            # 단어장 이름 복사하여 기존의 단어장 삭제, 생성, 단어 생성
            book = book_repo.find_one_by_id(share['book_id'])
            words = word_repo.find_all_by_book_id(share['book_id'])
            book_repo.delete(share['book_id'])
            book = book_repo.add(auth['id'], book['name'], share['id'])

            for word in words:
                word_repo.add(book['id'], word['word'], word['mean'])

            return custom_response("SUCCESS", data=words)
        except CustomException as e:
            return e.get_response()
        except:
            return custom_response("단어장 수정 실패", code=500)
        
    @staticmethod
    @ServiceReceiver.database
    def delete_book(auth, id, db: Database):
        try:
            book_repo = BookRepository(db)
            
            # 삭제할 데이터가 있는지 조회
            book = book_repo.find_one_by_id(id = id)
            
            if book is None:
                return custom_response("단어장이 이미 존재하지 않습니다.", code=404)
            
            # 권한 조회
            if book["user_id"] == auth["id"]:
                book_repo.delete(id=id)
                return custom_response("단어장 삭제 성공")
            else:
                CustomException("단어장 삭제 권한이 없습니다.", code=403)
        except CustomException as e:
            return e.get_response()
        except:
            return custom_response("단어장 삭제 실패", code=500)
        
    @staticmethod
    @ServiceReceiver.database
    def add_share_book(auth, data, db: Database):
        try:
            book_repo = BookRepository(db)
            share_repo = ShareRepository(db)
            
            # 공유할 단어장이 있는지 조회
            book = book_repo.find_one_by_id(id = data['id'])
            
            if book is None:
                raise CustomException("단어장이 존재하지 않습니다.", code=404)
            if book['is_shared']:
                raise CustomException("이미 공유 중인 단어장입니다.", code=409)
            if book['share_id']:
                raise CustomException("다운로드 받은 단어장입니다.", code=409)
            if book["user_id"] != auth["id"]:
                raise CustomException("단어장 제어 권한이 없습니다.", code=403)
            
            share_repo.add(book['id'], data['comment'])
            book = book_repo.update_is_shared(data['id'], True)
            
            return custom_response("단어장 공유 추가 성공", data=book)
        except CustomException as e:
            return e.get_response()
        except Exception as e:
            return custom_response("단어장 공유 추가 실패", code=500)
        
    @staticmethod
    @ServiceReceiver.database
    def delete_share_book(auth, data, db: Database):
        try:
            book_repo = BookRepository(db)
            share_repo = ShareRepository(db)
            
            # 공유할 단어장이 있는지 조회
            book = book_repo.find_one_by_id(id = data['id'])
    
            if book is None:
                raise CustomException("단어장이 존재하지 않습니다.", code=404)
            if book['share_id']:
                raise CustomException("다운로드 받은 단어장입니다.", code=409)
            if book["user_id"] != auth["id"]:
                raise CustomException("단어장 제어 권한이 없습니다.", code=403)
            share = share_repo.find_one_by_book_id(book['id'])
            book = book_repo.update_is_shared(data['id'], False)
            share = share_repo.delete(share['id'])

            return custom_response("단어장 공유 삭제 성공", data=book)
        except CustomException as e:
            return e.get_response()
        except Exception as e:
            return custom_response("단어장 공유 삭제 실패", code=500)