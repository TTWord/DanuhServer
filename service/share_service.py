from repository.share_repository import ShareRepository
from repository.book_repository import BookRepository
from db.connect import Database
from util.custom_response import custom_response
from util.decorator.service_receiver import ServiceReceiver
from util.exception import CustomException
from config import config
import requests
import json
from collections import defaultdict 


class ShareService:
    @staticmethod
    @ServiceReceiver.database
    def get_all_shared_books(db: Database):
        share_repo = ShareRepository(db)
        book_repo = BookRepository(db)

        all_share = share_repo.find_all()

        return custom_response("데이터 조회 성공", code=200, data=all_share)