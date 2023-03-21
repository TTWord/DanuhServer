from repository.user_repository import UserRepository
from repository.certification_repository import CertificationRepository
from util.decorator.service_receiver import ServiceReceiver
from util.custom_response import custom_response
from util.exception import CustomException
from util.jwt_token import generate_token
from util.password_encryption import compare_passwords, encrypt_password
from util.certification import EmailSender
from db.connect import Database
from config import config
import datetime
import random
from util.validation import validate_email, validate_password


class AuthService:
    @staticmethod
    @ServiceReceiver.database
    def signin_service(user_credentials, db: Database):
        try:
            user = UserRepository(db).find_one_by_username(user_credentials['username'])

            if not user:
                raise CustomException("유저가 존재하지 않습니다.", code=404)
            else:
                payload = {"id": user["id"], "username": user['username'],
                           'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)}
                secret = config["SECRET_KEY"]
                if compare_passwords(user_credentials['password'], user['password']):
                    token = {"access_token": generate_token(payload, secret)}
                    return custom_response("SUCCESS", data=token)
                else:
                    raise CustomException("유효하지 않은 비밀 번호입니다.", code=403)
        except CustomException as e:
            print("e : ", e)
            return e.get_response()
        except Exception as e:
            print("e2 : ", e)
            return custom_response("FAIL", code=400)

    @staticmethod
    @ServiceReceiver.database
    def send_mail(input_data, db: Database):
        try:
            user_repo = UserRepository(db)
            is_user = user_repo.find_one_by_username(input_data['username'])
            # vaildation
            if is_user:
                raise CustomException("이미 존재하는 유저입니다.", code=409)
            elif not validate_email(input_data['username']):
                raise CustomException("이메일 형식이 올바르지 않습니다.", code=400)
            elif not validate_password(input_data['password']):
                raise CustomException("8자 이상의 하나 이상의 숫자, 문자, 특수문자를 입력해주세요.", code=400)
            to_email = input_data['username']
            subject = config['STML_SUBJECT']
            body = config['STML_BODY']
            verification_id = str(random.randint(0, 999)).zfill(3) + str(random.randint(0, 999)).zfill(3)
            response = EmailSender.send_email(to_email, subject, body, verification_id)

            now = datetime.datetime.now()
            expiration_date = now + datetime.timedelta(days=1)
            expiration_date_str = expiration_date.strftime('%Y-%m-%d %H:%M:%S')
            verification_info = {
                'cert_type': 'email',
                'cert_key': input_data['username'],
                'cert_code': verification_id,
                'expired_time': expiration_date_str
            }
            if response[1] == 200:
                cert_repo = CertificationRepository(db)
                if cert_repo.find_one_by_cert_key(verification_info['cert_key']):
                    verification_id = cert_repo.update(verification_info['cert_key'], verification_info['cert_code'])
                else:
                    verification_id = cert_repo.add(verification_info)
                return custom_response("SUCCESS", data=verification_info)
        except CustomException as e:
            return e.get_response()
        except Exception as e:
            print(e)
            return custom_response("FAIL", code=400)