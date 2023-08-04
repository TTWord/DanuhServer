from repository.share_repository import ShareRepository
from repository.word_repository import WordRepository
from repository.book_repository import BookRepository
from repository.user_repository import UserRepository
from repository.recommend_repository import RecommendRepository
from repository.book_share_repository import BookShareRepository
from db.connect import Database
from util.custom_response import custom_response
from util.decorator.service_receiver import ServiceReceiver
from util.exception import CustomException
from util.time import get_difference_time
from util.sort import sorted_by_value
from collections import defaultdict


class ShareService:
    @staticmethod
    @ServiceReceiver.database
    def get_all_shared_books(data, db: Database):
        try:
            share_repo = ShareRepository(db)
            book_repo = BookRepository(db)
            user_repo = UserRepository(db)
            word_repo = WordRepository(db)

            all_share = share_repo.find_all()
            
            shares = []
            for share in all_share:
                book = book_repo.find_one_by_id(share['book_id'])
                share['book_name'] = book['name']
                share['updated_at'] = book['updated_at']

                user = user_repo.find_one_by_user_id(book['user_id'])
                share['nickname'] = user['nickname']

                # 책 이름이나 유저 이름에 검색값이 들어가는지 확인
                if data['name']:
                    if not (data['name'] in book['name'] or data['name'] in user['nickname']):
                        continue
                
                share['word_count'] = len(word_repo.find_all_by_book_id(book['id']))
                if data["type"] == "popularity":
                    share['popularity'] = share['downloaded'] + share['recommended']
                shares.append(share)

            order = True if data['order'] == "DESC" else False
            if data["type"] == "popularity":
                shares = sorted_by_value(shares, order, "popularity", "checked")
                [share.pop('popularity') for share in shares]
            else:
                shares = sorted_by_value(shares, order, data['type'])
            [share.pop('updated_at') for share in shares]
            [share.pop('checked') for share in shares]

            return custom_response("SUCCESS", code=200, data=shares)
        except CustomException as e:
            return e.get_response()
        except Exception as e:
            return custom_response("FAIL", code=500)
             
    @staticmethod
    @ServiceReceiver.database
    def get_share_by_id(id, db: Database):
        try:
            share_repo = ShareRepository(db)
            word_repo = WordRepository(db)
            book_repo = BookRepository(db)

            share = share_repo.find_one_by_id(id)
            if share is None:
                raise CustomException("SHARE_NOT_FOUND", code=409)
            words = word_repo.find_all_by_book_id(share['book_id'])

            # 데이터 가공
            book_id = share['book_id']
            book = book_repo.find_one_by_id(book_id)
            share_repo.update_column(id, 'checked')
            [word.pop('book_id') for word in words]
            data = {
                'user_id': book['user_id'],
                'book_id': book_id,
                'comment': share['comment'],
                'downloaded': share['downloaded'],
                'checked': share['checked'],
                'words': words
            }

            return custom_response("SUCCESS", data=data)
        except CustomException as e:
            return e.get_response()
        except Exception as e:
            return custom_response("FAIL", code=500)
        
    @staticmethod
    @ServiceReceiver.database
    def download_book(auth, data, db: Database):
        try:
            share_repo = ShareRepository(db)
            word_repo = WordRepository(db)
            book_repo = BookRepository(db)
            book_share_repo = BookShareRepository(db)
            
            share = share_repo.find_one_by_id(data['id'])
            if share is None:
                raise CustomException("SHARE_NOT_FOUND", code=409)
            elif not share['is_shared']:
                raise CustomException("BOOK_NOT_SHARED", code=409)
            
            # 본인의 단어장 여부
            book = book_repo.find_one_by_id(share['book_id'])
            if book['user_id'] == auth['id']:
                raise CustomException("SHARE_BOOK_OWNER", code=409)
            
            # 다운로드 되어 있는지 확인
            books = book_repo.find_all_by_user_id(auth['id'])
            count = 0
            for book in books:
                if book['is_downloaded']:
                    book_share = book_share_repo.find_one_by_book_id_and_share_id(book['id'], share['id'])
                    if book_share:
                        count += 1

            if count:
                raise CustomException("SHARE_ALREADY_EXIST", code=409)
            # 다운로드 증가, 다운로드 데이터 추가
            share_repo.update_column(share['id'], 'downloaded')

            # 단어장 이름 복사하여 단어장 생성, 단어 생성
            book = book_repo.find_one_by_id(share['book_id'])
            words = word_repo.find_all_by_book_id(share['book_id'])
            book = book_repo.add(auth['id'], book['name'], True)
            book_share_repo.add(book['id'], share['id'])

            for word in words:
                word_repo.add(book['id'], word['word'], word['mean'])
            return custom_response("SUCCESS", data=words)
        except CustomException as e:
            return e.get_response()
        except Exception as e:
            return custom_response("FAIL", code=500)

    @staticmethod
    @ServiceReceiver.database  
    def update_recommend_share(auth, id, db: Database):
        try:
            share_repo = ShareRepository(db)
            recommend_repo = RecommendRepository(db)

            share = share_repo.find_one_by_id(id)
            recommend = recommend_repo.find_one_by_like_user_id_and_book_id(auth['id'], share['book_id'])
            if share is None:
                raise CustomException("SHARE_NOT_FOUND", code=409)
            # 추천이 있는 경우 recommend 삭제, 공유 테이블 recommended -1
            if recommend:
                data = share_repo.update_column(share['id'], 'recommended', -1)
                recommend_repo.delete(recommend['id'])
            else:
                data = share_repo.update_column(share['id'], 'recommended')
                recommend_repo.add(auth['id'], share['book_id'])

            return custom_response("SUCCESS", data=data)
        except CustomException as e:
            return e.get_response()
        except Exception as e:
            return custom_response("FAIL", code=500)

    @staticmethod
    @ServiceReceiver.database
    def get_user_shared_books(auth, data, db: Database):
        try:
            share_repo = ShareRepository(db)
            book_repo = BookRepository(db)
            user_repo = UserRepository(db)
            word_repo = WordRepository(db)

            # 유저 별 조회
            books = book_repo.find_all_by_user_id(auth['id'])
            filter_books = []
            for book in books:
                share = share_repo.find_one_by_book_id(book['id'])

                if not share:
                    continue

                user = user_repo.find_one_by_user_id(book['user_id'])
                share['book_name'] = book['name']
                share['nickname'] = user['nickname']
                share['updated_at'] = book['updated_at']
                share['word_count'] = len(word_repo.find_all_by_book_id(book['id']))

                del share['is_shared'], share['comment']
                filter_books.append(share)

            order = True if data['order'] == "DESC" else False
            filter_books = sorted_by_value(filter_books, order, data['type'])

            [filter_book.pop('updated_at') for filter_book in filter_books]
            [filter_book.pop('checked') for filter_book in filter_books]
            return custom_response("SUCCESS", code=200, data=filter_books)
        except CustomException as e:
            return e.get_response()
        except Exception as e:
            return custom_response("FAIL", code=500)

    @staticmethod
    @ServiceReceiver.database
    def get_user_downloaded_books(auth, data, db: Database):
        try:
            share_repo = ShareRepository(db)
            book_repo = BookRepository(db)
            word_repo = WordRepository(db)
            user_repo = UserRepository(db)
            recommend_repo = RecommendRepository(db)
            book_share_repo = BookShareRepository(db)

            # 유저 별 조회
            books = book_repo.find_all_by_user_id(auth['id'])
            filter_books = []
            for book in books:
                book_share = book_share_repo.find_one_by_book_id(book['id'])

                if not book_share:
                    continue
                share = share_repo.find_one_by_id(book_share['share_id'])
                book = book_repo.find_one_by_id(share['book_id'])
                user = user_repo.find_one_by_user_id(book['user_id'])
                recommend = recommend_repo.find_one_by_like_user_id_and_book_id(auth['id'], book['id'])

                share['book_name'] = book['name']
                share['nickname'] = user['nickname']
                share['word_count'] = len(word_repo.find_all_by_book_id(book['id']))
                share['is_recommended'] = True if recommend else False
                share['updated_at'] = book['updated_at']
                del share['is_shared'], share['comment']

                if data['filter']:
                    if recommend:
                        filter_books.append(share)
                else:
                    filter_books.append(share)

            order = True if data['order'] == "DESC" else False
            filter_books = sorted_by_value(filter_books, order, data['type'])
            [filter_book.pop('updated_at') for filter_book in filter_books]
            [filter_book.pop('checked') for filter_book in filter_books]
            
            return custom_response("SUCCESS", code=200, data=filter_books)
        except CustomException as e:
            return e.get_response()
        except Exception as e:
            return custom_response("FAIL", code=500)
          
    @staticmethod
    @ServiceReceiver.database
    def get_other_user_shared_books(id, data, db: Database):
        try:
            share_repo = ShareRepository(db)
            book_repo = BookRepository(db)
            user_repo = UserRepository(db)
            word_repo = WordRepository(db)

            books = book_repo.find_all_by_user_id(id)
            book_ids = ",".join([str(book['id']) for book in books])
            shares = share_repo.find_all_by_book_id(book_ids)
            
            filter_shares = []
            for share in shares:
                book = book_repo.find_one_by_id(share['book_id'])
                share['book_name'] = book['name']

                user = user_repo.find_one_by_user_id(book['user_id'])
                share['nickname'] = user['nickname']
                
                words = word_repo.find_all_by_book_id(book['id'])
                share['word_count'] = len(words)
                share['updated_at'] = book['updated_at']

                del share['is_shared'], share['comment']

                if data["type"] == "popularity":
                    share['popularity'] = share['downloaded'] + share['recommended']
                
                filter_shares.append(share)

            order = True if data['order'] == "DESC" else False
            if data["type"] == "popularity":
                filter_shares = sorted_by_value(filter_shares, order, "popularity", "checked")
                [filter_share.pop('popularity') for filter_share in filter_shares]
            else:
                filter_shares = sorted_by_value(filter_shares, order, data['type'])
            [filter_share.pop('updated_at') for filter_share in filter_shares]
            [filter_share.pop('checked') for filter_share in filter_shares]
            return custom_response("SUCCESS", code=200, data=filter_shares)
        except CustomException as e:
            return e.get_response()
        except Exception as e:
            return custom_response("FAIL", code=500)