from db.connect import Connect
from model.user_model import UserModel


class FileRepository(Connect):
    def add(self, user_id: int, file_path: str) -> dict:
        sql = f"""
            INSERT INTO file (
                user_id,
                file_path
            )
            VALUES(
                {user_id},
                '{file_path}'
            );
        """
        self.cursor.execute(sql)
        self.connect.commit()

        
        return self.cursor.lastrowid
                
    def find_one_by_id(self, id: int) -> dict:
        sql = f'SELECT * FROM file WHERE id = {id}'
        self.cursor.execute(sql)
        file = self.cursor.fetchone()
        return file
    
    def find_one_by_user_id(self, user_id: int) -> dict:
        sql = f'SELECT * FROM file WHERE user_id = {user_id}'
        self.cursor.execute(sql)
        file = self.cursor.fetchone()
        return file
    
    def update(self, user_id: int, file_path: str) -> dict:
        sql = f"UPDATE file SET file_path='{file_path}' WHERE user_id = {user_id}"
        self.cursor.execute(sql)
        self.connect.commit()
        
        return id
        
    def delete(self, id: int):
        sql = f"DELETE FROM file WHERE id={id}"
        self.cursor.execute(sql)
        self.connect.commit()

        return {'id': id}