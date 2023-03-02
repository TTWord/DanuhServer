from util.password_encryption import encrypt_password, compare_passwords
from db.connect import Connect
from model.user_model import UserModel


class UserRepository(Connect): 
    # TODO : Send mail 추가
    def sign_up(self, user_info: dict) -> dict:        
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

    def get_user(self, user_id: str) -> dict:
        sql = f'SELECT * FROM user where username="{user_id}"'
        self.cursor.execute(sql)
        user = self.cursor.fetchone()
        
        return user