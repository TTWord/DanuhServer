class ShareModel:
    def __init__(self, id: int, book_id: int,  is_shared: bool = True, comment: str = "", checked: int = 0, downloaded: int = 0, recommended: int = 0):
        self.id = id
        self.book_id = book_id
        self.is_shared = bool(is_shared)
        self.comment = comment
        self.checked = checked
        self.downloaded = downloaded
        self.recommended = recommended

    def __repr__(self):
        return f"Shared({self.id}, {self.name})"