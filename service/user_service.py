from repository.user_repository import UserRepository
from flask import make_response
from db.connect import Database
from config import config
from util.jwt_token import generate_token
from util.password_encryption import compare_passwords, encrypt_password


# TODO: 상황에 따른 에러 메시지 
class UserService:
    @staticmethod
    def signup_service(user_data):
        try:
            db = Database()
            db.connect()
            is_user = UserRepository(db).get_user(user_data['username'])
            if is_user:
                return make_response({'message': 'user already exists'}, 409)
            user_data['password'] = encrypt_password(user_data['password']).decode('utf-8')
            UserRepository(db).sign_up(user_data)
            db.disconnect()
            return make_response({'message': 'succesfully inserted'}, 200)
        except Exception as e:
            return make_response({'message': str(e)}, 404)

    @staticmethod
    def signin_service(user_credentials):
        try:
            db = Database()
            db.connect()
            user = UserRepository(db).get_user(user_credentials['username'])
            db.disconnect()
            if not user:
                return make_response({'message': 'user isn\'t exist'}, 409)
            else:
                payload = {"username": user['username'], "id": str(user['id'])}
                secret = config["SECRET_KEY"]
                if compare_passwords(user_credentials['password'], user['password']):
                    token = generate_token(payload, secret)
                    return make_response({'token': token}, 200)
                else:
                    return make_response({'message': 'Invalid password'}, 403)

        except Exception as e:
            return make_response({'message': str(e)}, 404)
        
    @staticmethod
    def delete_service(user_data):
        try:
            db = Database()
            db.connect()
            UserRepository(db).delete(user_data['username'])
            db.disconnect()
            return make_response({'message': 'succesfully inserted'}, 200)
        except Exception as e:
            return make_response({'message': str(e)}, 404)