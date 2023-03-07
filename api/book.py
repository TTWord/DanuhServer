from service.book_service import BookService
from flask_restx import Namespace, Resource, Api, reqparse, fields
from util.decorator.authorization import Authorization


api = Namespace('book', description='단어장 API')

input_text = api.model('예측', {
    'text': fields.String(required=True, description='예측 값 입력', example='You can tell a stranger that this is shiitake mushrooms.')
})

# getBookParser = api.parser()
# getBookParser.add_argument('name', type=str, help='단어장 이름', location='args')
    
@api.route("/")
class Book(Resource):
    # @api.expect(getBookParser)
    @Authorization.get_authorization
    def get(self, auth):
        """
        모든 단어장 조회
        설명입니다
        """
        print(auth)
            
        return BookService.get_books_all()
    
    def post(self):
        return "add_book"
    
@api.route('/<int:id>')
class BookById(Resource):
    def get(self, id):
        return BookService.get_book_by_id(id)
    
    def put(self, id):
        return "update_book"
    
    def delete(self, id):
        return "delete_book"