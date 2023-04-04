from util.decorator.service_receiver import ServiceReceiver
from db.connect import Database

class QuizService:
    @staticmethod
    @ServiceReceiver.database
    def quiz_service(db: Database):
      try:
        pass
      except Exception as e:
        pass