from db.connect import Database, MongoDatabase


class ServiceReceiver:
    @staticmethod
    def database(func):
        def wrapper(*args, **kwargs):
            db = Database()
            db.connect()
            
            data = func(*args, **kwargs, db = db)
            
            db.disconnect()
            
            return data
          
        return wrapper
    
    @staticmethod
    def mongodb(func):
        def wrapper(*args, **kwargs):
            db = MongoDatabase()
            client = db.connect()
            
            data = func(*args, **kwargs, client = client)
            
            db.disconnect()
            
            return data
          
        return wrapper