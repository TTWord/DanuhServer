from repository.user_repository import UserRepository
from flask import make_response
from db.connect import Database


# 200 , 201, 204 성공
# 403, NOt forbbiden
# 404 Not Found
# 409 conflict 로그인 실패
# TODO: 상황에 따른 에러 메시지 
# 백엔드가 에러 메시지를 사용자에게 띄워주면 안됨
class UserService:
    @staticmethod
    def signup_service(userdata):
        db = Database()
        db.connect()
        response = UserRepository(db).find_user('123')
        UserRepository(db).signup(userdata)

        db.disconnect()
        # make_response({'message': 'succesfully inserted'}, 200)
                # except Exception as e:
        #     return make_response({'message': str(e)}, 404)
        # return jsonify(response)
        return make_response({'message': 'succesfully inserted'}, 200)

    def signin_service(user_credentials):
        db = Database()
        db.connect()

        response = UserRepository(db).find_user('123')

        db.disconnect()
        # try:
        #     email_check = User.objects[:1](email=user_credentials['email'])
        #     if not email_check:
        #         return {"status": 404, "message": "email does not exists"}
        #     else:
        #         for user in email_check:
        #             payload = {"email": user['email'], "_id": str(user['id']), 'exp': datetime.datetime.utcnow(
        #             ) + datetime.timedelta(minutes=60)}
        #             secret = os.environ.get('TOKEN_SECRET')
        #             if compare_passwords(user_credentials['password'], user['password']):
        #                 token = generate_token(payload, secret)
        #                 return make_response({'token': token}, 200)
        #             else:
        #                 return make_response({'message': 'Invalid password'}, 403)

        # except Exception as e:
        #     return make_response({'message': str(e)}, 404)
