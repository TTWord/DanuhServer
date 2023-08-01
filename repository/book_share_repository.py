from db.connect import Connect


class BookShareRepository(Connect):
    def add(self, book_id, share_id) -> dict:
        sql = f"""
            INSERT INTO book_share (
                book_id, share_id
            )
            VALUES(
                {book_id},
                {share_id}
            );
        """
        self.cursor.execute(sql)
        self.connect.commit()

        return {'book_share': self.cursor.lastrowid}
    
    def find_one_by_book_id_and_share_id(self, book_id: int, share_id: int) -> dict:
        sql = f'SELECT * FROM book_share WHERE book_id = {book_id} and share_id = {share_id};'
        self.cursor.execute(sql)
        book_share = self.cursor.fetchone()
        
        return book_share
    
    def find_one_by_book_id(self, book_id: int) -> dict:
        sql = f'SELECT * FROM book_share WHERE book_id = {book_id};'
        self.cursor.execute(sql)
        book_share = self.cursor.fetchone()
        
        return book_share
    
    def delete_book_id_and_share_id(self, book_id: int, share_id: int) -> dict:
        sql = f"DELETE FROM book_share WHERE like_user_id = {book_id} and book_id = {share_id}"
        self.cursor.execute(sql)
        self.connect.commit()
        
        return {'book_id': book_id, 'share_id': share_id}