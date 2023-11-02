class BookRecommendInfoModel:
    def __init__(self, id: int, name: str = None, share_id: int =None):
        self.id = id
        self.name = name
        self.share_id = share_id

    def __repr__(self):
        return f"Book({self.id}, {self.name})"