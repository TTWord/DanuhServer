from db.connect import Connect
from model.shared_model import SharedModel


class SharedRepository(Connect):
    def add(self, book_id: int, comment: str) -> dict:
        sql = f"""
            INSERT INTO shared (
                book_id,
                comment
            )
            VALUES(
                {book_id},
                '{comment}'
            );
        """
        self.cursor.execute(sql)
        self.connect.commit()

        shared = SharedModel(id=self.cursor.lastrowid, book_id=book_id,
                            comment=comment)

        return shared.__dict__
    
    def find_all(self) -> list:
        sql = 'SELECT * FROM shared'
        self.cursor.execute(sql)
        result = self.cursor.fetchall()

        return result
    
    def find_one_by_id(self, id: int) -> dict:
        shared = None

        sql = f'SELECT * FROM shared WHERE id = {id}'
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        if result is not None:
            shared = SharedModel(id=result['id'], book_id=result['book_id'],
                                comment=result['comment'])
            return shared.__dict__
        else:
            return None
        
    def find_one_by_book_id(self, book_id: int) -> dict:
        shared = None
        
        sql = f'SELECT * FROM shared WHERE book_id = "{book_id}"'
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        
        result = self.cursor.fetchone()
        if result is not None:
            shared = SharedModel(id=result['id'], book_id=result['book_id'],
                                comment=result['comment'])
            return shared.__dict__
        else:
            return None
        
    def delete(self, id: int) -> dict:
        sql = f"DELETE FROM book WHERE id = {id}"
        self.cursor.execute(sql)
        self.connect.commit()
        
        return {'id': id}