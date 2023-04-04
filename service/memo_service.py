from util.decorator.service_receiver import ServiceReceiver
from db.connect import Database

class MemoService:
    @staticmethod
    @ServiceReceiver.database
    def memo_service(db: Database):
      try:
        pass
      except Exception as e:
        pass