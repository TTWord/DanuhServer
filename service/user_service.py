from repository.user_repository import UserRepository
from util.password_encryption import encrypt_password, compare_passwords
from util.jwt_token import generate_token
from flask import make_response
import os
import datetime


class UserService:
    @staticmethod
    def signup_service(userdata):
        db = Database()
        db.connect()

        response = UserRepository(db).signup_service()

        db.disconnect()
        # make_response({'message': 'succesfully inserted'}, 200)
                # except Exception as e:
        #     return make_response({'message': str(e)}, 404)
        return jsonify(response)
        UserRepository().signup(userdata)
        return make_response({'message': 'succesfully inserted'}, 200)

    def signin_service(user_credentials):
        try:
            email_check = User.objects[:1](email=user_credentials['email'])
            if not email_check:
                return {"status": 404, "message": "email does not exists"}
            else:
                for user in email_check:
                    payload = {"email": user['email'], "_id": str(user['id']), 'exp': datetime.datetime.utcnow(
                    ) + datetime.timedelta(minutes=60)}
                    secret = os.environ.get('TOKEN_SECRET')
                    if compare_passwords(user_credentials['password'], user['password']):
                        token = generate_token(payload, secret)
                        return make_response({'token': token}, 200)
                    else:
                        return make_response({'message': 'Invalid password'}, 403)

        except Exception as e:
            return make_response({'message': str(e)}, 404)
