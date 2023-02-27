from config import Database

class Book:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return f"Book({self.id}, {self.name})"
    
    @staticmethod
    def get_books():
        db = Database()
        
        db.connect()
        
        books = []
        with db.connection.cursor() as cursor:
            sql = 'SELECT * FROM book'
            cursor.execute(sql)
            result = cursor.fetchall()
            
            for row in result:
                books.append(Book(id=row[0], name=row[2]))
        
        db.disconnect()
        
        return [book.__dict__ for book in books]