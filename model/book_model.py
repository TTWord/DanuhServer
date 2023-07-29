class BookModel:
    def __init__(self, id: int, name: str, user_id: int = None, is_downloaded: bool = False, created_at: str = None, updated_at: str = None):
        self.id = id
        self.name = name
        self.user_id = user_id
        self.is_downloaded = bool(is_downloaded)
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return f"Book({self.id}, {self.name})"