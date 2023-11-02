from db.connect import Connect
from model.book_model import BookModel
from model.response.share.book_recommend_info_model import BookRecommendInfoModel


class BookRepository(Connect):
    def find_all(self) -> list:
        books = []
        
        sql = 'SELECT * FROM book'
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        
        for row in result:
            books.append(BookModel(id=row['id'], name=row['name'], user_id=row['user_id'], 
                                   is_downloaded=row['is_downloaded'],
                                   created_at=row['created_at'], updated_at=row['updated_at'], word_count=row['word_count'], word_memorized_count=row['word_memorized_count'], start_view=row['start_view']))
        
        return [book.__dict__ for book in books]
    
    def find_all_by_user_id(self, user_id: int):
        books = []
        
        result = self.select_all(f'SELECT * FROM book WHERE user_id = {user_id}')
        
        for row in result:
            books.append(BookModel(id=row['id'], name=row['name'], user_id=row['user_id'], 
                                   is_downloaded=row['is_downloaded'],
                                   created_at=row['created_at'], updated_at=row['updated_at'], word_count=row['word_count'], word_memorized_count=row['word_memorized_count'], start_view=row['start_view']))
        
        return [book.__dict__ for book in books]
    
    def find_all_by_user_id_with_zero_start_view(self, user_id: int):
        books = []
        
        # start_view = 0 이면 최초 조회, 1이면 최초 조회가 아님
        result = self.select_all(f'''SELECT
                                    b.id,
                                    b.user_id,
                                    b.name,
                                    b.is_downloaded,
                                    b.created_at,
                                    b.updated_at,
                                    b.word_count,
                                    b.word_memorized_count,
                                    b.start_view,
                                    bs.share_id
                                FROM book AS b
                                INNER JOIN book_share AS bs 
                                ON b.id = bs.book_id
                                WHERE b.user_id = {user_id} and b.start_view = 0 and b.is_downloaded = 1''')
        
        for row in result:
            books.append(BookRecommendInfoModel(id=row['id'], name=row['name'], share_id=row['share_id']))
        
        return [book.__dict__ for book in books]
        
    
    def find_one_by_id(self, id: int) -> dict:
        book = None

        sql = f'SELECT * FROM book WHERE id = {id}'
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        if result is not None:
            book = BookModel(id=result['id'], name=result['name'], user_id=result['user_id'], 
                                   is_downloaded=result['is_downloaded'],
                                   created_at=result['created_at'], updated_at=result['updated_at'], word_count=result['word_count'], word_memorized_count=result['word_memorized_count'], start_view=result['start_view'])
            return book.__dict__
        else:
            return None
    
    def find_one_by_name_and_user_id(self, name: str, user_id: int) -> dict:
        book = None
        
        sql = f'SELECT * FROM book WHERE name = "{name}" AND user_id = {user_id}'
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        
        if result is not None:
            book = BookModel(id=result['id'], name=result['name'], user_id=result['user_id'], 
                                   is_downloaded=result['is_downloaded'],
                                   created_at=result['created_at'], updated_at=result['updated_at'], word_count=result['word_count'], word_memorized_count=result['word_memorized_count'], start_view=result['start_view'])
            return book
        else:
            return None
    
    def add(self, user_id: int, name: str, is_downloaded: bool = False, word_count: int = 0) -> dict:
        sql = f"INSERT INTO book (user_id, name, is_downloaded, word_count) VALUES ({user_id}, '{name}', {is_downloaded}, {word_count})"
        self.cursor.execute(sql)
        self.connect.commit()
        
        book = BookModel(id=self.cursor.lastrowid, user_id=user_id, name=name)
        
        return book.__dict__
    
    def update(self, id: int, name: str) -> dict:
        sql = f"UPDATE book SET name = '{name}' WHERE id = {id}"
        self.cursor.execute(sql)
        self.connect.commit()
        
        book = BookModel(id=id, name=name)
        
        return book.__dict__
    
    def update_start_view(self, id: int) -> dict:
        sql = f"UPDATE book SET start_view = 1 WHERE id = {id}"
        self.cursor.execute(sql)
        self.connect.commit()
        
        book = BookModel(id=id, start_view=1)
        
        return book.__dict__
        
    def delete(self, id: int) -> dict:
        sql = f"DELETE FROM book WHERE id = {id}"
        self.cursor.execute(sql)
        self.connect.commit()
        
        return {'id': id}
    
    def update_is_downloaded(self, id: int, is_downloaded: bool) -> dict:
        sql = f"UPDATE book SET is_downloaded = {is_downloaded} WHERE id = {id}"
        self.cursor.execute(sql)
        self.connect.commit()

        return {'id': id, 'is_downloaded': is_downloaded}
    
    #TODO 작업 남음
    def patch_book_word_count(self, id: int, count: int) -> dict:
        update_book_sql = f"UPDATE book SET word_count = {count} where id = {id}"
        self.cursor.execute(update_book_sql)
        self.connect.commit()
        
        return {'id': id, 'word_count': count}
    
    #TODO 작업 남음
    def patch_book_word_memorized_count(self, id: int, count: int) -> dict:
        update_book_sql = f"UPDATE book SET word_memorized_count = {count} where id = {id}"
        self.cursor.execute(update_book_sql)
        self.connect.commit()
        
        return {'id': id, 'word_memorized_count': count}