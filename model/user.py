from config import Database

class User:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return f"Book({self.id}, {self.name})"
    
    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = flask_bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password: str) -> bool:
        return flask_bcrypt.check_password_hash(self.password_hash, password)
    
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
                books.append(Book(id=row[0], name=row[1]))
        
        db.disconnect()
        
        return [book.__dict__ for book in books]