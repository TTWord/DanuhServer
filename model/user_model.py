class UserModel:
    def __init__(self, id: int, username: str, nickname: str = None, 
                 created_at: str = None, updated_at: str = None, file_id: int = None):
        self.id = id
        self.username = username
        self.nickname = nickname
        self.created_at = None
        self.updated_at = None
        self.file_id = file_id

    def __repr__(self):
        return f"User({self.id}, {self.username}, {self.nickname})"