class WordModel:
    def __init__(self, id: int, book_id: int, word: str, mean: str, created_at: str = None, updated_at: str = None):
        self.id = id
        self.book_id = book_id
        self.word = word
        self.mean = mean
        self.created_at = None
        self.updated_at = None

    def __repr__(self):
        return f"Word({self.id}, {self.name})"