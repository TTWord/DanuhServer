from db.connect import Connect


class UserRepository(Connect): 
    def sign_up(self, user_info: dict) -> dict:
        sql = f"""
            INSERT INTO user (
                username, password, nickname
            )
            VALUES(
                '{user_info['username']}',
                '{user_info['password']}',
                '{user_info['nickname']}'
            );
        """
        self.cursor.execute(sql)
        self.connect.commit()

    def delete(self, user_id: str) -> dict:
        sql = f"DELETE FROM user WHERE username = '{user_id}'"
        self.cursor.execute(sql)
        self.connect.commit()
        return {'id': id}
    
    def get_user(self, user_id: str) -> dict:
        sql = f'SELECT * FROM user where username="{user_id}"'
        self.cursor.execute(sql)
        user = self.cursor.fetchone()
        
        return user