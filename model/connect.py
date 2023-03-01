from config import Database


db = Database()

class Connect:
    def __init__(self):
        self.db = Database()
        self.connect = self.db.connect()
        self.cursor = self.db.connection.cursor()
    
    def __del__(self):
        self.db.disconnect()