from db.connect import Connect


class RecommendRepository(Connect):
    def add(self, like_user_id, book_id) -> dict:
        sql = f"""
            INSERT INTO recommend (
                like_user_id, book_id
            )
            VALUES(
                {like_user_id},
                {book_id}
            );
        """
        self.cursor.execute(sql)
        self.connect.commit()

        return {'recoommend_id': self.cursor.lastrowid}
    
    def find_one_by_like_user_id_and_book_id(self, like_user_id: int, book_id: int) -> dict:
        sql = f'SELECT * FROM recommend WHERE like_user_id = {like_user_id} and book_id = {book_id};'
        self.cursor.execute(sql)
        recommend = self.cursor.fetchone()
        
        return recommend
    
    def find_all_by_like_user_id(self, like_user_id: int) -> dict:
        sql = f'SELECT * FROM recommend WHERE like_user_id = {like_user_id};'
        self.cursor.execute(sql)
        recommend = self.cursor.fetchone()
        
        return recommend
    
    def delete_like_user_id_and_book_id(self, like_user_id: int, book_id: int) -> dict:
        sql = f"DELETE FROM recommend WHERE like_user_id = {like_user_id} and book_id = {book_id}"
        self.cursor.execute(sql)
        self.connect.commit()
        
        return {'like_user_id': like_user_id, 'book_id': book_id}
    
    def delete(self, id: int) -> dict:
        sql = f"DELETE FROM recommend WHERE id = {id}"
        self.cursor.execute(sql)
        self.connect.commit()
        
        return {'id': id}