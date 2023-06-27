from db.connect import Connect
from model.book_model import BookModel


class BookRepository(Connect):
    def find_all(self) -> list:
        books = []
        
        sql = 'SELECT * FROM book'
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        
        for row in result:
            books.append(BookModel(id=row['id'], name=row['name'], user_id=row['user_id'], 
                                   is_shared=row['is_shared'], is_downloaded=row['is_downloaded'],
                                   created_at=row['created_at'], updated_at=row['updated_at']))
        
        return [book.__dict__ for book in books]
    
    def find_all_by_user_id(self, user_id: int):
        books = []
        
        result = self.select_all(f'SELECT * FROM book WHERE user_id = {user_id}')
        
        for row in result:
            books.append(BookModel(id=row['id'], name=row['name'], user_id=row['user_id'], 
                                   is_shared=row['is_shared'], is_downloaded=row['is_downloaded'],
                                   created_at=row['created_at'], updated_at=row['updated_at']))
        
        return [book.__dict__ for book in books]
    
    def find_one_by_id(self, id: int) -> dict:
        book = None

        sql = f'SELECT * FROM book WHERE id = {id}'
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        if result is not None:
            book = BookModel(id=result['id'], name=result['name'], user_id=result['user_id'], 
                                   is_shared=result['is_shared'], is_downloaded=result['is_downloaded'],
                                   created_at=result['created_at'], updated_at=result['updated_at'])
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
                                   is_shared=result['is_shared'], is_downloaded=result['is_downloaded'],
                                   created_at=result['created_at'], updated_at=result['updated_at'])
            return book
        else:
            return None
    
    def add(self, user_id: int, name: str) -> dict:
        sql = f"INSERT INTO book (user_id, name) VALUES ({user_id}, '{name}')"
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
        
    def delete(self, id: int) -> dict:
        sql = f"DELETE FROM book WHERE id = {id}"
        self.cursor.execute(sql)
        self.connect.commit()
        
        return {'id': id}
    
    def update_shared(self, id: int, is_shared: bool) -> dict:
        sql = f"UPDATE book SET is_shared = {is_shared} WHERE id = {id}"
        self.cursor.execute(sql)
        self.connect.commit()

        return {'id': id, 'is_shared': is_shared}