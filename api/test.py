from service.share_service import ShareService
from flask_restx import Namespace, Resource, Api, reqparse, fields
from util.decorator.authorization import Authorization
from flask import request
from util.decorator.logging import logging
from PIL import Image
import pytesseract
from util.custom_response import custom_response
from werkzeug.datastructures import FileStorage
from pdf2image import convert_from_bytes


api = Namespace('test', description='테스트 API')

pdf = api.parser()
pdf.add_argument("file", type=FileStorage, location="files")
pdf.add_argument('page', type=int, help='page number', location='form')


@api.route("")
@api.doc(security="Bearer Auth")
class Share(Resource):
    @api.response(200, "SUCCESS")
    @api.response(409, "FILE_UNEXPECTED_EXTENSION")
    @api.response(500, "FAIL")
    @api.expect(pdf)
    @logging
    # @Authorization.check_authorization
    # def post(self, auth):
    def post(self):
        """
        공유 단어장 다운로드
        """
        file = request.files["file"]
        page = request.form["page"]

        pdf_content = file.read()
        images = convert_from_bytes(pdf_content)

        txt = pytesseract.image_to_string(images[int(page)], lang='kor+eng').encode("utf-8")

        return custom_response("SUCCESS", code=200, data=txt.decode('utf-8'))