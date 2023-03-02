from util.password_encryption import encrypt_password, compare_passwords
from db.connect import Connect
from model.user_model import UserModel

# TODO : Model_info 클래스 객체
#      : model 폴더에 생성
class UserRepository(Connect):    
    def signup(self, user_info: dict) -> dict:        
        password = encrypt_password(user_info['password']).decode('utf-8')
        sql = f"""
            INSERT INTO user (
                username, password, nickname
            )
            VALUES(
                '{user_info['username']}',
                '{password}',
                '{user_info['nickname']}'
            );
        """
        self.cursor.execute(sql)
        self.connect.commit()

    def find_user(self, user_id: str) -> dict:
        # users = []
        # with self.cursor as cursor:
        #     sql = f"""
        #     SELECT username, password 
        #     FROM user 
        #     WHERE username = '{user_id}'
        #     """
        #     cursor.execute(sql)
        #     result = self.cursor.fetchone()
    
        # return [user.__dict__ for user in users]
        users = []
        sql = 'SELECT * FROM user'
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        
        for row in result:
            users.append(UserModel(id=row['id'], username=row['username'], nickname=row['nickname']))
        
        return [user.__dict__ for user in users]