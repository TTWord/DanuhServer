class BookModel:
    def __init__(self, id: int, name: str, user_id: int = None, is_shared: bool = False, downloaded_id: int = 0, created_at: str = None, updated_at: str = None):
        self.id = id
        self.name = name
        self.user_id = user_id
        self.is_shared = is_shared
        self.downloaded_id = downloaded_id
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return f"Book({self.id}, {self.name})"