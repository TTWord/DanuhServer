from repository.user_repository import UserRepository
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
            cert_info = UserRepository(db).auth_find_one_by_cert_key(user_data['username'])
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
    def delete(user_data, db: Database):
        try:
            user = UserRepository(db).find_one_by_username(user_data['username'])
            if not user:
                raise CustomException("유저가 존재하지 않습니다.", code=404)
            user = UserRepository(db).delete(user_data['username'])
            return custom_response("SUCCESS", data=user)
        except CustomException as e:
            return e.get_response()
        except Exception as e:
            return custom_response("FAIL", code=400)