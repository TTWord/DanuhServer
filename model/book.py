from model.connect import Connect
    
class BookModel(Connect):
    def find_all(self):
        books = []
        
        with self.cursor as cursor:
            sql = 'SELECT * FROM book'
            cursor.execute(sql)
            result = cursor.fetchall()
            
            for row in result:
                books.append(Book(id=row['id'], name=row['name']))
        
        return [book.__dict__ for book in books]
    
    def find_by_id(self, id):
        book = None

        with self.cursor as cursor:
            sql = f'SELECT * FROM book WHERE id = {id}'
            cursor.execute(sql)
            result = cursor.fetchone()
            
            book = Book(id=result['id'], name=result['name'])
            
        return book.__dict__

class Book:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return f"Book({self.id}, {self.name})"