from db.connect import Connect
from model.user_model import UserModel


class FileRepository(Connect):
    def add(self, fild_info: dict) -> dict:
        sql = f"""
            INSERT INTO file (
                file_path
            )
            VALUES(
                '{fild_info['file_path']}'
            );
        """
        self.cursor.execute(sql)
        self.connect.commit()
        
        return fild_info
                
    def find_one_by_id(self, id: int) -> dict:
        sql = f'SELECT * FROM file WHERE id = {id}'
        self.cursor.execute(sql)
        file = self.cursor.fetchone()
        return file
    
    def update(self, id: int, file_path: str) -> dict:
        sql = f"UPDATE file SET file_path='{file_path}' WHERE id = {id}"
        self.cursor.execute(sql)
        self.connect.commit()
        
        return file_path
        
    def delete(self, id: int):
        sql = f"DELETE FROM file WHERE id={id}"
        self.cursor.execute(sql)
        self.connect.commit()

        return {'id': id}