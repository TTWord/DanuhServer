from db.connect import Connect
from model.user_model import UserModel


class UserRepository(Connect): 
    def add(self, user_info: dict) -> dict:
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
        user = UserModel(id=self.cursor.lastrowid, username=user_info['username'], 
                         nickname=user_info['nickname'])
        
        return user.__dict__

    def delete(self, id: str) -> dict:
        sql = f"DELETE FROM user WHERE id = '{id}'"
        self.cursor.execute(sql)
        self.connect.commit()

        return {'id': id}

    def find_one_by_username(self, user_name: str) -> dict:
        sql = f'SELECT * FROM user where username = "{user_name}"'
        self.cursor.execute(sql)
        result = self.cursor.fetchone()

        return result
    
    def find_one_by_user_id(self, id: int) -> dict:
        sql = f'SELECT * FROM user where id = "{id}"'
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        
        if result:
            user = UserModel(id=result['id'], username=result['username'], 
                             nickname=result['nickname'], file_id=result['file_id'])
            return user.__dict__
        else:
            return None
    
    def update(self, id: int, username: str, password: str, nickname: str) -> dict:
        sql = f"UPDATE user SET password={password}, nickname='{nickname}' WHERE id = {id}"
        self.cursor.execute(sql)
        self.connect.commit()
        
        user = UserModel(id=id, username=username, nickname=nickname)
        
        return user.__dict__
    
    def update_nickname(self, id: int, nickname: str) -> dict:
        sql = f"UPDATE user SET nickname='{nickname}' WHERE id = {id}"
        self.cursor.execute(sql)
        self.connect.commit()
        
        return {'nickname': nickname}
    
    def update_file_id(self, id: int, file_id: int) -> dict:
        sql = f"UPDATE user SET file_id={file_id} WHERE id = {id}"
        self.cursor.execute(sql)
        self.connect.commit()
        return {'file_id': file_id}