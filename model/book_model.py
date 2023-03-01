class BookModel:
    def __init__(self, id: int, name: str, user_id: int = None, created_at: str = None, updated_at: str = None):
        self.id = id
        self.name = name
        self.user_id = user_id
        self.created_at = None
        self.updated_at = None

    def __repr__(self):
        return f"Book({self.id}, {self.name})"