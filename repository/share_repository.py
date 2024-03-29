from db.connect import Connect
from model.share_model import ShareModel


class ShareRepository(Connect):
    def add(self, book_id: int, comment: str) -> dict:
        sql = f"""
            INSERT INTO share (
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

        shared = ShareModel(id=self.cursor.lastrowid, book_id=book_id,
                            comment=comment)

        return shared.__dict__
    
    def find_all(self) -> list:
        shares = []
        sql = f"SELECT * FROM share"

        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        for row in result:
            shares.append(ShareModel(id=row['id'], book_id=row['book_id'], is_shared=row['is_shared'],
                                comment=row['comment'], checked=row['checked'],
                                downloaded=row['downloaded'], recommended=row['recommended']))
        
        return [share.__dict__ for share in shares]

    def find_all_by_book_id(self, book_id: str = "") -> list:
        sql = f"SELECT * FROM share WHERE book_id IN ({book_id})"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()

        return result
    
    def find_one_by_id(self, id: int) -> dict:
        shared = None

        sql = f'SELECT * FROM share WHERE id = {id}'
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        if result is not None:
            shared = ShareModel(id=result['id'], book_id=result['book_id'], is_shared= result['is_shared'],
                                comment=result['comment'], checked=result['checked'],
                                downloaded=result['downloaded'], recommended=result['recommended'])
            return shared.__dict__
        else:
            return None
        
    def find_one_by_book_id(self, book_id: int) -> dict:
        shared = None
        
        sql = f'SELECT * FROM share WHERE book_id = "{book_id}"'
        self.cursor.execute(sql)        
        result = self.cursor.fetchone()
        
        if result is not None:
            shared = ShareModel(id=result['id'], book_id=result['book_id'], is_shared=result['is_shared'],
                                comment=result['comment'], checked=result['checked'],
                                downloaded=result['downloaded'], recommended=result['recommended'])
            return shared.__dict__
        else:
            return None
        
    def delete(self, id: int) -> dict:
        sql = f"DELETE FROM share WHERE id = {id}"
        self.cursor.execute(sql)
        self.connect.commit()
        
        return {'id': id}
    
    def update_column(self, id: int, col: str, number: int = 1) -> dict:        
        sql = f"UPDATE share SET {col} = {col} + {number} WHERE id={id}"
        self.cursor.execute(sql)
        self.connect.commit()
        
        return {'id': id, 'recommend': number}
    
    def update_comment(self, id: int, comment: str) -> dict:        
        sql = f"UPDATE share SET comment = '{comment}' WHERE id={id}"
        self.cursor.execute(sql)
        self.connect.commit()
        
        return {'id': id, 'comment': comment}
    
    def update_is_shared(self, id: int, is_shared: bool) -> dict:        
        sql = f"UPDATE share SET is_shared = {is_shared} WHERE id = {id}"
        self.cursor.execute(sql)
        self.connect.commit()

        return {'id': id, 'is_shared': is_shared}