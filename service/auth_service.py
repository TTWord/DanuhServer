from repository.user_repository import UserRepository
from repository.certification_repository import CertificationRepository
from util.decorator.service_receiver import ServiceReceiver
from util.custom_response import custom_response
from util.exception import CustomException
from util.jwt_token import generate_token, decode_token
from util.password_encryption import compare_passwords, encrypt_password
from util.certification import EmailSender
from util.validation import validate_email, validate_password
from db.connect import Database
from config import config
import datetime
import random
import requests


class AuthService:
    @staticmethod
    @ServiceReceiver.database
    def signin_service(user_credentials, db: Database):
        try:
            user = UserRepository(db).find_one_by_username(user_credentials['username'])

            if not user:
                raise CustomException("유저가 존재하지 않습니다.", code=404)
            else:
                payload_access = {"id": user["id"], "username": user['username'],
                           'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}
                payload_reflash = {"id": user["id"], "username": user['username'],
                           'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=6)}
                secret = config["SECRET_KEY"]
                if compare_passwords(user_credentials['password'], user['password']):
                    token = {"access_token": generate_token(payload_access, secret),
                             "refresh_token": generate_token(payload_reflash, secret)}
                    return custom_response("SUCCESS", data=token)
                else:
                    raise CustomException("유효하지 않은 비밀 번호입니다.", code=403)
        except CustomException as e:
            return e.get_response()
        except Exception as e:
            return custom_response("FAIL", code=400)
        
    @staticmethod
    def signin_with_kakao_service():
        CLIENT_ID = config['CLIENT_ID']
        REDIRECT_URI = config['REDIRECT_URI']
        return custom_response("SUCCESS", 
                               data={
                                'url': "https://kauth.kakao.com/oauth/authorize?client_id=%s&redirect_uri=%s&response_type=code" \
                                % (CLIENT_ID, REDIRECT_URI)})
    @staticmethod
    @ServiceReceiver.database
    def oauth_api(code, db: Database):
        auth_server = "https://kauth.kakao.com%s"
        api_server = "https://kapi.kakao.com%s"
        default_header = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Cache-Control": "no-cache",
        }
        CLIENT_ID = config['CLIENT_ID']
        CLIENT_SECRET = config['CLIENT_SECRET']
        REDIRECT_URI = config['REDIRECT_URI']
        auth_info = requests.post(
            url=auth_server % "/oauth/token", 
            headers=default_header,
            data={
                "grant_type": "authorization_code",
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "redirect_uri": REDIRECT_URI,
                "code": code,
            }, 
        ).json()
        bearer_token = 'bearer ' + auth_info["access_token"]
        print(bearer_token)
        default_header = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        kakao_info = requests.post(
            url=api_server % "/v2/user/me", 
            headers={
                **default_header,
                **{"Authorization": bearer_token}
            },
            #"property_keys":'["kakao_account.profile_image_url"]'
            data={}
        ).json()
        # id = 카카오 아이디, nickname = 카카오 닉네임
        user_refo = UserRepository(db)
        user = user_refo.find_one_by_username(kakao_info['id'])
        if not user:
            data = {
                'username': str(kakao_info['id']),
                'password': encrypt_password(str(kakao_info['id'])).decode('utf-8'),
                'nickname': kakao_info['properties']['nickname'],
            }
            print("data : ", data)
            user = user_refo.add(data)
        payload_access = {"id": user["id"], "username": user['username'],
                            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}
        payload_reflash = {"id": user["id"], "username": user['username'],
                            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=6)}
        secret = config["SECRET_KEY"]
        token = {"access_token": generate_token(payload_access, secret),
                    "refresh_token": generate_token(payload_reflash, secret)}
        return custom_response("SUCCESS", data=token)


    @staticmethod
    @ServiceReceiver.database
    def send_mail(input_data, db: Database):
        try:
            user_repo = UserRepository(db)
            is_username = user_repo.find_one_by_username(input_data['username'])
            is_nickname =user_repo.find_one_by_nickname(input_data['nickname'])
            if is_nickname:
                raise CustomException("이미 존재하는 닉네임입니다.", code=409)
            
            if is_username:
                raise CustomException("이미 존재하는 유저입니다.", code=409)
            elif not validate_email(input_data['username']):
                raise CustomException("이메일 형식이 올바르지 않습니다.", code=400)
            elif not validate_password(input_data['password']):
                raise CustomException("암호는 8자 이상의 하나 이상의 숫자, 문자, 특수문자이어야 합니다.", code=400)
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
            return custom_response("FAIL", code=400)
        
    @staticmethod
    def get_new_access_token(auth):
        payload_access = {"id": auth["id"], "username": auth['username'],
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}
        secret = config["SECRET_KEY"]
        token = {"access_token": generate_token(payload_access, secret)}
        return custom_response("SUCCESS", data=token)
    

