class WordModel:
    def __init__(self, id: int, book_id: int, word: str, mean: str, is_memorized: bool = False, created_at: str = None, updated_at: str = None):
        self.id = id
        self.book_id = book_id
        self.word = word
        self.mean = mean
        self.is_memorized = is_memorized
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return f"Word({self.id}, {self.name})"