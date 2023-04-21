from db.connect import Database


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