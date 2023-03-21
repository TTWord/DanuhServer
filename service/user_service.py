from repository.user_repository import UserRepository
from repository.certification_repository import CertificationRepository
from util.decorator.service_receiver import ServiceReceiver
from util.custom_response import custom_response
from util.exception import CustomException
from util.password_encryption import compare_passwords, encrypt_password
from db.connect import Database


class UserService:
    @staticmethod
    @ServiceReceiver.database
    def signup_service(user_data, db: Database):
        try:
            cert_info = CertificationRepository(db).find_one_by_cert_key(user_data['username'])
            if not cert_info['cert_code'] == user_data['certification_id']:
                raise CustomException("인증 코드가 동일하지 않습니다.", code=403)
            user_data['password'] = encrypt_password(user_data['password']).decode('utf-8')
            UserRepository(db).add(user_data)
            return custom_response("SUCCESS")
        except CustomException as e:
            return e.get_response()
        except Exception as e:
            return custom_response("FAIL", code=400)
    
    @staticmethod
    @ServiceReceiver.database
    def update_user(id, user_data, db: Database):
        try:
            user_repo = UserRepository(db)
            user = user_repo.find_one_by_user_id(id)
            if not user:
                raise CustomException("유저가 존재하지 않습니다.", code=404)
            user_data['password'] = encrypt_password(user_data['password']).decode('utf-8')
            user = user_repo.update(id, user_data['username'], user_data['password'], user_data['nickname'])
            return custom_response("SUCCESS", data=user)
        except CustomException as e:
            return e.get_response()
        except Exception as e:
            return custom_response("FAIL", code=400)
        
    @staticmethod
    @ServiceReceiver.database
    def delete_user_by_username(user_data, db: Database):
        try:
            user_repo = UserRepository(db)
            user = user_repo.find_one_by_username(user_data['username'])
            if not user:
                raise CustomException("유저가 존재하지 않습니다.", code=404)
            user = user_repo.delete(user['id'])
            return custom_response("SUCCESS", data=user)
        except CustomException as e:
            return e.get_response()
        except Exception as e:
            return custom_response("FAIL", code=400)
        
    @staticmethod
    @ServiceReceiver.database
    def delete_user_by_id(id, db: Database):
        try:
            user_info = UserRepository(db)
            user = user_info.find_one_by_user_id(id)
            if not user:
                raise CustomException("유저가 존재하지 않습니다.", code=404)
            user = UserRepository(db).delete(user['id'])
            return custom_response("SUCCESS", data=user)
        except CustomException as e:
            return e.get_response()
        except Exception as e:
            return custom_response("FAIL", code=400)