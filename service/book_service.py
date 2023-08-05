from repository.book_repository import BookRepository
from repository.word_repository import WordRepository
from repository.share_repository import ShareRepository
from repository.book_share_repository import BookShareRepository
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
        book_repo = BookRepository(db).find_all()
        share_repo = ShareRepository(db)
        
        books = book_repo.find_all()
        for book in books:
            share = share_repo.find_one_by_book_id(book['id'])
            if share:
                book['is_sharing'] = True
                book['comment'] = share['comment']

        return { "code" : 200, "data" : books }
    
    @staticmethod
    @ServiceReceiver.database
    def get_books_by_user_id(auth, db: Database):
        try:
            book_repo = BookRepository(db)
            share_repo = ShareRepository(db)

            books = book_repo.find_all_by_user_id(user_id = auth['id'])
            for book in books:
                share = share_repo.find_one_by_book_id(book['id'])
                if share:
                    book['is_sharing'] = True
                    book['comment'] = share['comment']

            return custom_response("SUCCESS", data=books)
        except Exception as e:

            return custom_response("FAIL", code=500)
    
    @staticmethod
    @ServiceReceiver.database
    def get_book_by_id(auth, id, db: Database):
        try:
            share_repo = ShareRepository(db)
            book_repo = BookRepository(db)

            book = book_repo.find_one_by_id(id)
            
            if book is None:
                raise CustomException("BOOK_NOT_FOUND", code=404)
            
            if book["user_id"] != auth["id"]:
                raise CustomException("BOOK_ACCESS_DENIED", code=403)
            
            share = share_repo.find_one_by_book_id(book['id'])
            if share:
                book['is_sharing'] = True
                book['comment'] = share['comment']
            return custom_response("SUCCESS", code=200, data=book)
        except CustomException as e:
            return e.get_response()
        except Exception as e:
            return custom_response("FAIL", code=500)
    
    @staticmethod
    @ServiceReceiver.database
    def add_book(auth, data, db: Database):
        try:
            if data["name"] is None:
                raise CustomException("BOOK_NOT_HAS_NAME", code=404)
            
            book_repo = BookRepository(db)
            
            # 데이터 중복 검사
            book = book_repo.find_one_by_name_and_user_id(name = data["name"], user_id = auth['id'])
            if book:
                raise CustomException("BOOK_DUPLICATE_NAME", code=409)
            
            book = book_repo.add(user_id = auth['id'], name = data["name"])
            
            return custom_response("SUCCESS", data=book)
        except CustomException as e:
            return e.get_response()
        except:
            return custom_response("FAIL", code=500)
        
    @staticmethod
    @ServiceReceiver.database
    def generate_book(auth, data, db: Database):
        try:
            url = f"{config['AI_IP']}"
            response = requests.post(url, json=data)
            result = json.loads(response.content)
            if data["name"] is None:
                raise CustomException("BOOK_NOT_HAS_NAME", code=404)

            book_repo = BookRepository(db)
            
            # 데이터 중복 검사
            book = book_repo.find_one_by_name_and_user_id(name = data["name"], user_id = auth['id'])
            
            if book is not None:
                raise CustomException("BOOK_ALREADY_EXIST", code=409)
            
            book = book_repo.add(user_id = auth['id'], name = data["name"])

            book_id = book["id"]
            word_repo = WordRepository(db)

            dict_check = defaultdict(str)
            
            word_len = 0
            books = book_repo.find_all_by_user_id(auth['id'])
            for book in books:
                word_len += len(word_repo.find_all_by_book_id(book['id']))

            if word_len + len(result['words']) > 200:
                raise CustomException("WORD_MORE_THAN_LIMIT", code=409)
            
            for word, mean in result['words'].items():
                if word not in dict_check.keys() and mean != dict_check[word]:
                    dict_check[word] = mean
 
            for word, mean in result['words'].items():
                word_repo.add(book_id, word, mean)

            return custom_response("SUCCESS", data=book)
        except CustomException as e:
            return e.get_response()
        except Exception as e:
            return custom_response("FAIL", code=500)
        
    @staticmethod
    @ServiceReceiver.database
    def update_book(auth, id, data, db: Database):
        try:
            if data["name"] is None:
                raise CustomException("BOOK_NOT_HAS_NAME", code=404)

            book_repo = BookRepository(db)
            
            # 변경할 데이터가 있는지 조회
            book = book_repo.find_one_by_id(id = id)
            
            # 데이터가 없을 경우
            if book is None:
                raise CustomException("BOOK_NOT_FOUND", code=404)
            
            # 같은 유저에 같은 이름을 가진 단어장이 있는지 체크
            same_book = book_repo.find_one_by_name_and_user_id(name = data["name"], user_id = auth['id'])
            
            # 중복 체크
            if same_book is not None:
                raise CustomException("BOOK_ALREADY_EXIST", code=409)
            
            # 유저 ID 검사
            if book["user_id"] != auth["id"]:
                raise CustomException("BOOK_ACCESS_DENIED", code=403)
            
            book = book_repo.update(id = id, name = data["name"])
            
            return custom_response("SUCCESS", data=book)
        except CustomException as e:
            return e.get_response()
        except:
            return custom_response("FAIL", code=500)
            
    @staticmethod
    @ServiceReceiver.database
    def update_share_book(auth, id, db: Database):
        try:
            book_repo = BookRepository(db)
            share_repo = ShareRepository(db)
            word_repo = WordRepository(db)
            book_share_repo = BookShareRepository(db)

            # 변경할 데이터가 있는지 조회
            book = book_repo.find_one_by_id(id = id)

            if auth['id'] != book['user_id']:
                raise CustomException("BOOK_ACCESS_DENIED", code=403)
            # 데이터가 없을 경우
            if book is None:
                raise CustomException("BOOK_NOT_FOUND", code=404)
            
            if book['is_downloaded'] is None:
                raise CustomException("BOOK_NOT_DOWNLOADED", code=409)
            
            book_share = book_share_repo.find_one_by_book_id(id)
            share = share_repo.find_one_by_book_id(book_share['share_id'])

            # 다운로드 증가
            share_repo.update_column(book_share['share_id'], 'downloaded')

            # 단어장 이름 복사하여 기존의 단어장 삭제, 생성, 단어 생성
            share_book = book_repo.find_one_by_id(share['book_id'])
            words = word_repo.find_all_by_book_id(share_book['book_id'])
            book_repo.delete(id)
            book = book_repo.add(auth['id'], share_book['name'], True)

            for word in words:
                word_repo.add(book['id'], word['word'], word['mean'])

            return custom_response("SUCCESS", data=words)
        except CustomException as e:
            return e.get_response()
        except:
            return custom_response("FAIL", code=500)
        
    @staticmethod
    @ServiceReceiver.database
    def delete_book(auth, id, db: Database):
        try:
            book_repo = BookRepository(db)
            
            # 삭제할 데이터가 있는지 조회
            book = book_repo.find_one_by_id(id = id)
            
            if book is None:
                return custom_response("BOOK_NOT_FOUND", code=404)
            
            # 권한 조회
            if book["user_id"] == auth["id"]:
                book_repo.delete(id=id)
                return custom_response("SUCCESS")
            else:
                raise CustomException("BOOK_ACCESS_DENIED", code=403)
        except CustomException as e:
            return e.get_response()
        except:
            return custom_response("FAIL", code=500)

    @staticmethod
    @ServiceReceiver.database
    def share_book(auth, data, db: Database):
        try:
            book_repo = BookRepository(db)
            share_repo = ShareRepository(db)
            
            # 공유할 단어장이 있는지 조회
            book = book_repo.find_one_by_id(id = data['id'])
            if book is None:
                raise CustomException("BOOK_NOT_FOUND", code=404)
            if book['is_downloaded']:
                raise CustomException("BOOK_DOWNLOADED", code=409)
            if book["user_id"] != auth["id"]:
                raise CustomException("BOOK_ACCESS_DENIED", code=403)

            share = share_repo.find_one_by_book_id(data['id'])
            if len(data['comment']) > 200:
                raise CustomException("SHARE_COMMENT_UPPER_THAN_LIMIT", code=409)
            
            # 공유 상태 추가한 경우
            if share:
                if data['share']:
                    # 변경할 comment가 다른 경우만 동작
                    if data['comment'] != share['comment']:
                        share_repo.update_comment(share['id'], data['comment'])

                    if not share['is_shared']:
                        share_repo.update_is_shared(share['id'], data['share'])

                    book = {'id': book['id'], 'is_shared': data['share']}
                # 공유 -> 비공유
                else:
                    share = share_repo.update_is_shared(share['id'], data['share'])
                    book = {'id': book['id'], 'is_shared': data['share']}
            # 추가한 적 없는 경우
            else:
                # 비공유 -> 공유 comment 상관 x
                if data['share']:
                    share_repo.add(book['id'], data['comment'])
                    book = {'id': book['id'], 'is_shared': data['share']}
                # 비공유 -> 비공유 동작 x
                else:
                    book = {'id': book['id'], 'is_shared': data['share']}
                    
            return custom_response("SUCCESS", data=book)
        except CustomException as e:
            return e.get_response()
        except Exception as e:
            return custom_response("FAIL", code=500)