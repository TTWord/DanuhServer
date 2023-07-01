from repository.share_repository import ShareRepository
from repository.word_repository import WordRepository
from repository.book_repository import BookRepository
from repository.user_repository import UserRepository
from db.connect import Database
from util.custom_response import custom_response
from util.decorator.service_receiver import ServiceReceiver
from util.exception import CustomException
from util.time import get_difference_time


class ShareService:
    @staticmethod
    @ServiceReceiver.database
    def get_all_shared_books(data, db: Database):
        share_repo = ShareRepository(db)
        book_repo = BookRepository(db)
        user_repo = UserRepository(db)

        if not data['type']:
            data['type'] = 'downloaded'
        if not data['order']:
            data['order'] = 'DESC'

        all_share = share_repo.find_all(data['type'], data['order'])

        shares = []
        for share in all_share:
            book = book_repo.find_one_by_id(share['book_id'])
            share['book_name'] = book['name']

            user = user_repo.find_one_by_user_id(book['user_id'])
            share['nickname'] = user['nickname']

            # 책 이름이나 유저 이름에 검색값이 들어가는지 확인
            if data['name']:
                if not (data['name'] in book['name'] or data['name'] in user['nickname']):
                    continue
                    
            share['updated_at'] = get_difference_time(book['updated_at'])
            shares.append(share)

        return custom_response("데이터 조회 성공", code=200, data=shares)
        
    @staticmethod
    @ServiceReceiver.database
    def get_share_by_id(id, db: Database):
        try:
            share_repo = ShareRepository(db)
            word_repo = WordRepository(db)

            share = share_repo.find_one_by_id(id)
            if share is None:
                raise CustomException("공유되지 않은 단어장입니다.", code=409)
            words = word_repo.find_all_by_book_id(share['book_id'])

            # 데이터 가공
            book_id = words[0]['book_id']
            share_repo.update_column(id, 'checked')
            [word.pop('book_id') for word in words]
            data = {
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
            
            share = share_repo.find_one_by_id(data['id'])
            if share is None:
                raise CustomException("공유되지 않은 단어장입니다.", code=409)
            
            # 본인의 단어장 여부
            book = book_repo.find_one_by_id(share['book_id'])
            if book['user_id'] == auth['id']:
                raise CustomException("본인의 단어장은 다운로드 받을 수 없습니다.", code=409)

            # 다운로드 증가
            share_repo.update_column(share['id'], 'downloaded')

            # 단어장 이름 복사하여 단어장 생성, 단어 생성
            book = book_repo.find_one_by_id(share['book_id'])
            words = word_repo.find_all_by_book_id(share['book_id'])
            book = book_repo.add(auth['id'], book['name'], share['id'])

            for word in words:
                word_repo.add(book['id'], word['word'], word['mean'])

            return custom_response("SUCCESS", data=words)
        except CustomException as e:
            return e.get_response()
        except Exception as e:
            return custom_response("FAIL", code=500)
        
    @staticmethod
    @ServiceReceiver.database
    def update_downloaded_book(auth, data, db: Database):
        try:
            share_repo = ShareRepository(db)
            word_repo = WordRepository(db)
            book_repo = BookRepository(db)
            
            share = share_repo.find_one_by_id(data['id'])
            if share is None:
                raise CustomException("공유되지 않은 단어장입니다.", code=409)
            
            # 다운로드 증가
            share_repo.update_column(share['id'], 'downloaded')

            # 단어장 이름 복사하여 단어장 생성, 단어 생성
            book = book_repo.find_one_by_id(share['book_id'])
            words = word_repo.find_all_by_book_id(share['book_id'])
            book = book_repo.add(auth['id'], book['name'], True)

            for word in words:
                word_repo.add(book['id'], word['word'], word['mean'])

            return custom_response("SUCCESS", data=words)
        except CustomException as e:
            return e.get_response()
        except Exception as e:
            return custom_response("FAIL", code=500)