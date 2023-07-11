from repository.user_repository import UserRepository
from repository.file_repository import FileRepository
from repository.book_repository import BookRepository
from repository.word_repository import WordRepository
from repository.share_repository import ShareRepository
from util.decorator.service_receiver import ServiceReceiver
from util.custom_response import custom_response
from util.exception import CustomException
from util.password_encryption import compare_passwords, encrypt_password
from util.validation import validate_password
from config import config
from db.connect import Database
from werkzeug.utils import secure_filename
from flask import url_for
import os


class UserService:
    @staticmethod
    @ServiceReceiver.database
    def get_user_by_id(id, db: Database):
        try:
            user_repo = UserRepository(db)
            user = user_repo.find_one_by_user_id(id)
            if not user:
                raise CustomException("유저가 존재하지 않습니다.", code=409)
            return custom_response("SUCCESS", data=user)
        except CustomException as e:
            return e.get_response()
        except Exception as e:
            return custom_response("FAIL", code=500)

    @staticmethod
    @ServiceReceiver.database
    def update_user(auth, data, db: Database):
        try:
            user_repo = UserRepository(db)
            user = user_repo.find_one_by_user_id(auth['id'])

            if not user:
                raise CustomException("유저가 존재하지 않습니다.", code=409)
            
            if not compare_passwords(data['from_password'], user['password']):
                raise CustomException("기존 비밀번호가 일치하지 않습니다.", code=409)
            
            if not validate_password(data['to_password']):
                raise CustomException("비밀번호 양식이 유효하지 않습니다.", code=409)

            if data['from_password'] == data['to_password']:
                raise CustomException("현재 비밀번호와 바꿀 비밀번호가 동일합니다.", code=409)
            
            new_password = encrypt_password(data["to_password"]).decode("utf-8")
            user = user_repo.update(auth['id'], user["username"], new_password, user["nickname"])
            return custom_response("SUCCESS", data=user)
        except CustomException as e:
            return e.get_response()
        except Exception as e:
            return custom_response("FAIL", code=500)

    @staticmethod
    @ServiceReceiver.database
    def delete_user_by_username(user_data, db: Database):
        try:
            user_repo = UserRepository(db)
            file_repo = FileRepository(db)
            user = user_repo.find_one_by_username(user_data["username"])
            if not user:
                raise CustomException("유저가 존재하지 않습니다.", code=409)
            
            file = file_repo.find_one_by_user_id(user['id'])
            if file:
                os.remove(config["PROFILE_IMAGE"] + "/" + file['file_path'])

            user = user_repo.delete(user["id"])
            return custom_response("SUCCESS", data=user)
        except CustomException as e:
            return e.get_response()
        except Exception as e:
            return custom_response("FAIL", code=500)

    @staticmethod
    @ServiceReceiver.database
    def delete_user_by_id(id, db: Database):
        try:
            user_repo = UserRepository(db)
            file_repo = FileRepository(db)

            user = user_repo.find_one_by_user_id(id)
            if not user:
                raise CustomException("유저가 존재하지 않습니다.", code=409)
            
            file = file_repo.find_one_by_user_id(user['id'])
            if file:
                os.remove(config["PROFILE_IMAGE"] + "/" + file['file_path'])

            user = user_repo.delete(user["id"])
            return custom_response("SUCCESS", data=user)
        except CustomException as e:
            return e.get_response()
        except Exception as e:
            return custom_response("FAIL", code=500)

    @staticmethod
    @ServiceReceiver.database
    def update_user_by_nickname(auth, data, db: Database):
        try:
            user_repo = UserRepository(db)
            user = user_repo.find_one_by_user_id(auth["id"])
            if user["nickname"] == data["to_nickname"]:
                raise CustomException("닉네임이 중복입니다.", code=409)
            user = user_repo.update_nickname(user["id"], data["to_nickname"])
            return custom_response("SUCCESS", data=user)
        except CustomException as e:
            return e.get_response()
        except Exception as e:
            return custom_response("FAIL", code=500)

    @staticmethod
    @ServiceReceiver.database
    def update_user_profile(auth, data, db: Database):
        try:
            file_repo = FileRepository(db)

            file_name = str(auth["id"]) + "_profile.jpg"
            file_path = config["PROFILE_IMAGE"] + "/" + secure_filename(file_name)
            data.save(file_path)

            file = file_repo.find_one_by_user_id(auth["id"])
            if file:
                file_repo.update(file['user_id'], secure_filename(file_name))
            else:
                file_repo.add(auth['id'], secure_filename(file_name))
            url = {"url": config["DOMAIN"] + "/" + file_path}
            return custom_response("SUCCESS", data=url)
        except CustomException as e:
            return e.get_response()
        except Exception as e:
            return custom_response("FAIL", code=500)

    @staticmethod
    @ServiceReceiver.database
    def get_user_profile(auth, db: Database):
        try:
            user_repo = UserRepository(db)
            file_repo = FileRepository(db)
            book_repo = BookRepository(db)
            word_repo = WordRepository(db)
            share_repo = ShareRepository(db)

            user = user_repo.find_one_by_user_id(auth["id"])
            books = book_repo.find_all_by_user_id(auth['id'])
            
            word_count = 0
            share_count = 0
            download_count = 0
            recommend_count = 0
            for book in books:
                word_count += len(word_repo.find_all_by_book_id(book['id']))
                if book['is_shared']:
                    share_count += 1
                    share = share_repo.find_one_by_book_id(book['id'])
                    download_count += share['downloaded']
                    recommend_count += share['recommended']

            info = {"id": auth['id'], "username": user["username"], "nickname": user["nickname"]}
            
            file = file_repo.find_one_by_user_id(auth['id'])
            if file:
                info.update({"url": config["DOMAIN"]
                            + url_for("static", filename=file["file_path"])})
                                 
            info.update(
                {
                    "word_count": word_count,
                    "share_count": share_count,
                    "download_count": download_count,
                    "recommend_count": recommend_count
                }
            )
            return custom_response("SUCCESS", data=info)
        except CustomException as e:
            return e.get_response()
        except Exception as e:
            return custom_response("FAIL", code=500)
