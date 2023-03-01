from config import Database
from utils.passwordEncryption import encrypt_password


class UserDao:
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
    
    def create_user(self, user_info, connection):
        db = Database()
        
        db.connect()
        
        with db.connection.cursor() as cursor:
            query = """
                INSERT INTO 
            """