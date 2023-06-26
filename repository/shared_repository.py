from db.connect import Connect
from model.shared_model import SharedModel


class SharedRepository(Connect):
    def find_all(self) -> list:
        sql = 'SELECT * FROM shared'
        self.cursor.execute(sql)
        result = self.cursor.fetchall()

        return result