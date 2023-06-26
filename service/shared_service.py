from repository.shared_repository import SharedRepository
from db.connect import Database
from util.custom_response import custom_response
from util.decorator.service_receiver import ServiceReceiver
from util.exception import CustomException
from config import config
import requests
import json
from collections import defaultdict 


class SharedService:
    @staticmethod
    @ServiceReceiver.database
    def get_all_shared_books(db: Database):
        shared = SharedRepository(db).find_all()
        
        return custom_response("데이터 조회 성공", code=200, data=shared)