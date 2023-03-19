from db.connect import Database

class ServiceReceiver:
    @staticmethod
    def database(func):
        def wrapper(*args, **kwargs):
            db = Database()
            db.connect()
            
            data = func(db = db, *args, **kwargs)
            
            db.disconnect()
            
            return data
          
        return wrapper