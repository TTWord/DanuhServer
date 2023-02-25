import pymysql
from dotenv import dotenv_values

# load ENV
config = dotenv_values(".env")

class Database:
    def __init__(self):
        self.host = config["DB_HOST"]
        self.user = config["DB_USER"]
        self.password = config["DB_PASSWORD"]
        self.database = config["DB_NAME"]
    
    def __repr__(self):
        return f"Database({self.host}, {self.user}, {self.password}, {self.database})"
      
    def connect(self):
        self.connection = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database, charset='utf8mb4')

    def disconnect(self):
        self.connection.close()