import pymysql
from pymongo import MongoClient
from config import config


class Database:
    def __init__(self):
        self.host = config["DB_HOST"]
        self.user = config["DB_USER"]
        self.password = config["DB_PASSWORD"]
        self.database = config["DB_NAME"]
    
    def __repr__(self):
        return f"Database({self.host}, {self.user}, {self.password}, {self.database})"
      
    def connect(self):
        self.connection = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        return self.connection

    def disconnect(self):
        self.connection.close()


class Connect:
    def __init__(self, database):
        self.connect = database.connection
        self.cursor = self.connect.cursor()
        
    def select_all(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()
        
    def select(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchone()
    

class MongoDatabase:
    def __init__(self):
        self.host = config["MONGODB_HOST"]
        self.user = config["DB_USER"]
        self.password = config["DB_PASSWORD"]
    
    def __repr__(self):
        return f"MongoDatabase({self.host, self.user, self.password})"
      
    def connect(self):
        self.client = MongoClient(self.host, username=self.user, password=self.password)
        return self.client

    def disconnect(self):
        self.client.close()
