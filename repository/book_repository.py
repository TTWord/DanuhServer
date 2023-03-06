from db.connect import Connect
from model.book_model import BookModel
from util.decorator.exporter import RepositoryExporter as exporter

class BookRepository(Connect):
    @exporter
    def find_all(self) -> list:
        books = []
        
        sql = 'SELECT * FROM book'
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        
        for row in result:
            books.append(BookModel(id=row['id'], name=row['name']))
        
        return books
    
    @exporter
    def find_all_by_user_id(self, user_id: int):
        books = []
        
        result = self.select_all('SELECT * FROM book WHERE user_id = {user_id}')
        
        for row in result:
            books.append(BookModel(id=row['id'], name=row['name']))
        
        return books
    
    @exporter
    def find_one_by_id(self, id: int) -> dict:
        book = None

        sql = f'SELECT * FROM book WHERE id = {id}'
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
            
        book = BookModel(id=result['id'], name=result['name'])
            
        return book
    
    @exporter
    def add(self, name: str) -> dict:
        sql = f"INSERT INTO book (name) VALUES ('{name}')"
        self.cursor.execute(sql)
        self.connection.commit()
        
        book = BookModel(id=self.cursor.lastrowid, name=name)
        
        return book
    
    @exporter
    def update(self, id: int, name: str) -> dict:
        sql = f"UPDATE book SET name = '{name}' WHERE id = {id}"
        self.cursor.execute(sql)
        self.connection.commit()
        
        book = BookModel(id=id, name=name)
        
        return book
        
    @exporter
    def delete(self, id: int):
        sql = f"DELETE FROM book WHERE id = {id}"
        self.cursor.execute(sql)
        self.connection.commit()
        
        return {'id': id}