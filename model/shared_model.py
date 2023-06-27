class SharedModel:
    def __init__(self, id: int, book_id: int, comment: str, checked: int = 0, downloaded: int = 0):
        self.id = id
        self.book_id = book_id
        self.comment = comment
        self.checked = checked
        self.downloaded = downloaded

    def __repr__(self):
        return f"Shared({self.id}, {self.name})"