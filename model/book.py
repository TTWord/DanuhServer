from db.connect import Connect, Database
    
class Book:
    def __init__(self, id: int, name: str, user_id: int = None, created_at: str = None, updated_at: str = None):
        self.id = id
        self.name = name
        self.user_id = user_id
        self.created_at = None
        self.updated_at = None

    def __repr__(self):
        return f"Book({self.id}, {self.name})"

class BookModel(Connect):
    def find_all(self) -> list:
        books = []
        
        sql = 'SELECT * FROM book'
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        
        for row in result:
            books.append(Book(id=row['id'], name=row['name']))
        
        return [book.__dict__ for book in books]
    
    def find_all_by_user_id(self, user_id: int):
        books = []
        
        result = self.select_all('SELECT * FROM book WHERE user_id = {user_id}')
        
        for row in result:
            books.append(Book(id=row['id'], name=row['name']))
        
        return [book.__dict__ for book in books]
    
    def find_one_by_id(self, id: int) -> dict:
        book = None

        sql = f'SELECT * FROM book WHERE id = {id}'
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
            
        book = Book(id=result['id'], name=result['name'])
            
        return book.__dict__
    
    def add(self, name: str) -> dict:
        sql = f"INSERT INTO book (name) VALUES ('{name}')"
        self.cursor.execute(sql)
        self.connection.commit()
        
        book = Book(id=self.cursor.lastrowid, name=name)
        
        return book.__dict__
    
    def update(self, id: int, name: str) -> dict:
        sql = f"UPDATE book SET name = '{name}' WHERE id = {id}"
        self.cursor.execute(sql)
        self.connection.commit()
        
        book = Book(id=id, name=name)
        
        return book.__dict__
        
    def delete(self, id: int):
        sql = f"DELETE FROM book WHERE id = {id}"
        self.cursor.execute(sql)
        self.connection.commit()
        
        return {'id': id}