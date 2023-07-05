from db.connect import Connect


class RecommendRepository(Connect):
    def add(self, recommend_info: dict) -> dict:
        sql = f"""
            INSERT INTO recommend (
                like_user_id, book_id
            )
            VALUES(
                {recommend_info['like_user_id']},
                {recommend_info['book_id']}
            );
        """
        self.cursor.execute(sql)
        self.connect.commit()

        return {'recommend_id': recommend_info["cert_code"]}
    
    def find_one_by_like_user_id_and_book_id(self, like_user_id: int, book_id: int) -> dict:
        sql = f'SELECT * FROM recommend WHERE like_user_id = {like_user_id} and book_id = {book_id};'
        self.cursor.execute(sql)
        recommend = self.cursor.fetchone()
        
        return recommend
    
    def delete(self, like_user_id: int, book_id: int) -> dict:
        sql = f"DELETE FROM recommend WHERE like_user_id = {like_user_id} and book_id = {book_id}"
        self.cursor.execute(sql)
        self.connect.commit()
        
        return {'like_user_id': like_user_id, 'book_id': book_id}