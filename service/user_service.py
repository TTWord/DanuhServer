from repository.user_repository import UserRepository
from flask import make_response
from db.connect import Database
from config import config
from util.jwt_token import generate_token, decode_token
from util.password_encryption import compare_passwords, encrypt_password
from util.mail import EmailSender
import datetime


class UserService:
    # TODO: 메일 인증 추가, 인증 실패, 인증성공
    @staticmethod
    def signup_service(user_data):
        try:
            db = Database()
            with db.connect():
                user_data['password'] = encrypt_password(user_data['password']).decode('utf-8')
                UserRepository(db).sign_up(user_data)
            return make_response({'message': 'Succesfully inserted'}, 200)
        except Exception as e:
            return make_response({'message': str(e)}, 404)

    @staticmethod
    def signin_service(user_credentials):
        try:
            db = Database()
            with db.connect():
                user = UserRepository(db).get_user(user_credentials['username'])

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
    def authorization_get(header):
        if header == None:
            return make_response({'message': 'Please login'}, 404)
        secret = config["SECRET_KEY"]
        data = decode_token(header, secret)
        return make_response(data, 200)
    

    # TODO : 추후 refectoring 필요(struecture 변경)
    @staticmethod
    def send_mail(input_data):
        db = Database()
        with db.connect():
            is_user = UserRepository(db).get_user(input_data['user_id'])
            if is_user:
                return make_response({'message': 'User already exists'}, 409)
        to_email = input_data['to_email']
        subject = input_data['subject']
        body = input_data['body']

        return make_response(EmailSender.send_email(to_email, subject, body))