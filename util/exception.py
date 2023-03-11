class CustomException(Exception):
    def __init__(self, comment, code=400, data=None):
        super(CustomException, self).__init__(comment)
        self.comment = comment
        self.code = code
        self.data = data

    def get_response(self):
        return {'code': int(self.code), 'comment': str(self.comment), 'data': self.data}