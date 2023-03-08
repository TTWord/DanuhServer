from repository.user_repository import UserRepository
from flask import make_response
from db.connect import Database
from config import config
from util.jwt_token import generate_token
from util.password_encryption import compare_passwords, encrypt_password
from util.certification import EmailSender
import datetime
import random


class UserService:
    @staticmethod
    def signup_service(user_data):
        try:
            db = Database()
            with db.connect():
                cert_info = UserRepository(db).auth_find_one_by_cert_key(user_data['username'])
                if not cert_info['cert_code'] == user_data['certification_id']:
                    return make_response({'message': 'Invalid verification code'}, 401 )
                user_data['password'] = encrypt_password(user_data['password']).decode('utf-8')
                UserRepository(db).add(user_data)
            return make_response({'message': 'Succesfully inserted'}, 200)
        except Exception as e:
            return make_response({'message': str(e)}, 404)

    @staticmethod
    def signin_service(user_credentials):
        try:
            db = Database()
            with db.connect():
                user = UserRepository(db).find_one_by_username(user_credentials['username'])

            if not user:
                return make_response({'message': 'User isn\'t exist'}, 409)
            else:
                payload = {"username": user['username'],
                           'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)}
                secret = config["SECRET_KEY"]
                if compare_passwords(user_credentials['password'], user['password']):
                    token = generate_token(payload, secret)
                    return make_response({'message': 'Succesfully login',
                                          'access_token': token}, 200)
                else:
                    return make_response({'message': 'Invalid password'}, 403)

        except Exception as e:
            return make_response({'message': str(e)}, 404)
        
    @staticmethod
    def delete_service(user_data):
        try:
            db = Database()
            with db.connect():
                UserRepository(db).delete(user_data['username'])
            return make_response({'message': 'Succesfully deleted'}, 200)
        except Exception as e:
            return make_response({'message': str(e)}, 404)    

    # TODO : 추후 refectoring 필요(struecture 변경)
    @staticmethod
    def send_mail(input_data):
        db = Database()
        with db.connect():
            is_user = UserRepository(db).find_one_by_username(input_data['user_id'])
            if is_user:
                return make_response({'message': 'User already exists'}, 409)
            to_email = input_data['to_email']
            subject = input_data['subject']
            body = input_data['body']
            verification_id = str(random.randint(0, 999)).zfill(3) + str(random.randint(0, 999)).zfill(3)
            response = EmailSender.send_email(to_email, subject, body, verification_id)

            now = datetime.datetime.now()
            expiration_date = now + datetime.timedelta(days=1)
            expiration_date_str = expiration_date.strftime('%Y-%m-%d %H:%M:%S')
            verification_info = {
                'cert_type': 'email',
                'cert_key': input_data['user_id'],
                'cert_code': verification_id,
                'expired_time': expiration_date_str
            }
            if response[1] == 200:
                if UserRepository(db).auth_find_one_by_cert_key(verification_info['cert_key']):
                    verification_id = UserRepository(db).auth_update(verification_info['cert_key'], verification_info['cert_code'])
                else:
                    verification_id = UserRepository(db).auth_add(verification_info)
                return make_response({**verification_id, 'message': 'Succesfully send email'}, 200)
        return make_response(response)