from repository.user_repository import UserRepository
from repository.certification_repository import CertificationRepository
from util.decorator.service_receiver import ServiceReceiver
from util.custom_response import custom_response
from util.exception import CustomException
from util.jwt_token import generate_token, decode_token
from util.password_encryption import compare_passwords, encrypt_password
from util.certification import EmailSender, OAuth
from util.validation import validate_email, validate_password
from db.connect import Database
from config import config
from datetime import datetime, timedelta
import random
from flask import redirect


class AuthService:
    @staticmethod
    @ServiceReceiver.database
    def signin_service(data, db: Database):
        try:
            user = UserRepository(db).find_one_by_username(data["username"])

            if not user:
                raise CustomException("USER_NOT_FOUND", code=409)
            else:
                payload_access = {
                    "id": user["id"],
                    "username": user["username"],
                    "exp": datetime.utcnow() + timedelta(minutes=30),
                }
                payload_refresh = {
                    "id": user["id"],
                    "username": user["username"],
                    "exp": datetime.utcnow() + timedelta(hours=6),
                }
                secret = config["SECRET_KEY"]
                if compare_passwords(data["password"], user["password"]):
                    token = {
                        "access_token": generate_token(payload_access, secret),
                        "refresh_token": generate_token(payload_refresh, secret),
                    }
                    return custom_response("SUCCESS", data=token)
                else:
                    raise CustomException("AUTH_ACCESS_FAILD", code=409)
        except CustomException as e:
            return e.get_response()
        except Exception as e:
            return custom_response("FAIL", code=500)

    @staticmethod
    def signin_with_social_service(service):
        CLIENT_ID = config[f"{service.upper()}_CLIENT_ID"]
        REDIRECT_URI = config["REDIRECT_URI"] + "/" + service.lower()
        if service == "kakao":
            url = {
                "url": "https://kauth.kakao.com/oauth/authorize?client_id=%s&redirect_uri=%s&response_type=code"
                % (CLIENT_ID, REDIRECT_URI)
            }
        elif service == "google":
            url = {
                "url": "https://accounts.google.com/o/oauth2/v2/auth?client_id=%s&redirect_uri=%s&response_type=code&scope=email profile"
                % (CLIENT_ID, REDIRECT_URI)
            }

        return custom_response("SUCCESS", data=url)

    @staticmethod
    @ServiceReceiver.database
    def social_auth_api(service, code, db: Database):
        try:
            # 전달받은 authorization code를 통해서 access_token을 발급
            service = service.lower()

            oauth = OAuth(service)
            auth_info = oauth.auth(code)

            # error 발생 시 로그인 페이지로 redirect
            if "error" in auth_info:
                raise CustomException("AUTH_ACCESS_FAILD", code=409)

            info = oauth.userinfo("Bearer " + auth_info["access_token"])

            user_refo = UserRepository(db)

            if service == "kakao":
                username = str(info["kakao_account"]["email"])
                password = encrypt_password(str(info["id"])).decode("utf-8")
                nickname = info["properties"]["nickname"] + str(info["id"])[:4]
            elif service == "google":
                username = str(info["email"])
                password = encrypt_password(str(info["email"])).decode("utf-8")
                nickname = info["name"] +info["id"][:4]
            # TODO: APPLE 로그인 추가
            elif service == "apple":
                username = str(info["sub"])
                password = encrypt_password(str(info["sub"])).decode("utf-8")
                nickname = info["email"]
            user = user_refo.find_one_by_username(username)

            is_member = "1"
            if not user:
                data = {
                    "username": username,
                    "password": password,
                    "nickname": nickname,
                    "login_type": service
                }
                user = user_refo.add(data)
                is_member = "0"
            else:
                # 유저가 존재하며 서비스가 다른 경우
                if user['login_type'] != service:
                    raise CustomException("USER_ALREADY_REGISTERED", code=409, data={"service": service})
            
            payload_access = {
                "id": user["id"],
                "username": user["username"],
                "exp": datetime.utcnow() + timedelta(minutes=30),
            }
            payload_reflash = {
                "id": user["id"],
                "username": user["username"],
                "exp": datetime.utcnow() + timedelta(hours=6),
            }
            secret = config["SECRET_KEY"]
            token = {
                "access_token": generate_token(payload_access, secret),
                "refresh_token": generate_token(payload_reflash, secret),
            }
            REDIRECT_URI_SOCIAL = config["REDIRECT_URI_SOCIAL"]

            return redirect(
                REDIRECT_URI_SOCIAL
                + "?accesstoken="
                + token["access_token"]
                + "&refreshtoken="
                + token["refresh_token"]
                + "&ismember="
                + is_member
            )
        except CustomException as e:
            return e.get_response()
        except Exception as e:
            return custom_response("FAIL", code=500)

    @staticmethod
    @ServiceReceiver.database
    def check_nickname(data, db: Database):
        nickname = data["nickname"]

        if not nickname:
            raise CustomException("USER_INVALID_USERNAME", code=409)
        user = UserRepository(db).find_one_by_nickname(nickname)

        if user is not None:
            raise CustomException("USER_DUPLICATE_NICKNAME", code=409)

        return custom_response("SUCCESS")

    @staticmethod
    @ServiceReceiver.database
    def send_mail(input_data, db: Database):
        try:
            user_repo = UserRepository(db)
            is_username = user_repo.find_one_by_username(input_data["username"])

            if is_username:
                # 이미 존재하는 유저입니다
                raise CustomException("USER_DUPLICATE_USERNAME", code=409)
            elif not validate_email(input_data["username"]):
                # 유효하지 않은 이메일 형식
                raise CustomException("USER_INVALID_FORMAT_USERNAME", code=409)
            elif not validate_password(input_data["password"]):
                # 유효하지 않은 비밀번호 형식 (암호는 8자 이상의 하나 이상의 숫자, 문자, 특수문자이어야 합니다)
                raise CustomException("USER_INVALID_FORMAT_PASSWORD", code=409)
            to_email = input_data["username"]
            subject = config["STML_SUBJECT"]
            body = config["STML_BODY"]
            verification_id = str(random.randint(0, 999)).zfill(3) + str(
                random.randint(0, 999)
            ).zfill(3)
            response = EmailSender.send_email(to_email, subject, body, verification_id)

            now = datetime.now()
            expiration_date = now + timedelta(minutes=3)
            expiration_date_str = expiration_date.strftime("%Y-%m-%d %H:%M:%S")
            verification_info = {
                "cert_type": "email",
                "cert_key": input_data["username"],
                "cert_code": verification_id,
                "expired_time": expiration_date_str,
            }
            if response[1] == 200:
                cert_repo = CertificationRepository(db)
                if cert_repo.find_one_by_cert_key(verification_info["cert_key"]):
                    verification_id = cert_repo.update(
                        verification_info["cert_key"],
                        verification_info["cert_code"],
                        verification_info["expired_time"],
                    )
                else:
                    verification_id = cert_repo.add(verification_info)
                return custom_response("SUCCESS", data=verification_info)
        except CustomException as e:
            return e.get_response()
        except Exception as e:
            return custom_response("FAIL", code=500)

    @staticmethod
    @ServiceReceiver.database
    def signup_service(data, db: Database):
        try:
            cert_repo = CertificationRepository(db)
            user_repo = UserRepository(db)
            cert_info = cert_repo.find_one_by_cert_key(data["username"])

            if cert_info["expired_time"] < datetime.now():
                # 인증코드 만료
                raise CustomException("AUTH_EXPIRED_CODE", code=403)
            elif not cert_info["cert_code"] == data["certification_id"]:
                # 인증코드 불일치
                raise CustomException("AUTH_INCORRECT_CODE", code=403)

            data["password"] = encrypt_password(data["password"]).decode("utf-8")
            data.update({"login_type": "local"})
            user = user_repo.add(data)

            cert_repo.update_user_id(user["username"], user['id'])
            payload_access = {
                    "id": user["id"],
                    "username": user["username"],
                    "exp": datetime.utcnow() + timedelta(minutes=30),
                }
            payload_refresh = {
                "id": user["id"],
                "username": user["username"],
                "exp": datetime.utcnow() + timedelta(hours=6),
            }
            secret = config["SECRET_KEY"]
            token = {
                "access_token": generate_token(payload_access, secret),
                "refresh_token": generate_token(payload_refresh, secret),
            }
            
            return custom_response("SUCCESS", data=token)
        except CustomException as e:
            return e.get_response()
        except Exception as e:
            return custom_response("FAIL", code=500)

    @staticmethod
    def get_new_access_token(auth):
        payload_access = {
            "id": auth["id"],
            "username": auth["username"],
            "exp": datetime.utcnow() + timedelta(minutes=30),
        }
        secret = config["SECRET_KEY"]
        token = {"access_token": generate_token(payload_access, secret)}
        return custom_response("SUCCESS", data=token)
