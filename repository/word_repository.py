from db.connect import Connect
from model.word_model import WordModel


class WordRepository(Connect):    
    def find_all_by_book_id(self, book_id: int):
        words = []
        sql = f'SELECT * FROM word WHERE book_id={book_id}'
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        for row in result:
            words.append(WordModel(id=row['id'], book_id=row['book_id'], word=row['word']
                         , mean=row['mean'], created_at=row['created_at'], updated_at=row['updated_at']))
        
        return [word.__dict__ for word in words]
                
    def find_one_by_id(self, id: int) -> dict:
        word = None

        sql = f'SELECT * FROM word WHERE id = {id}'
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        if result is not None:
            word = WordModel(id=result['id'], book_id=result['book_id'], word=result['word']
                         , mean=result['mean'], created_at=result['created_at'], updated_at=result['updated_at'])
            return word.__dict__
        else:
            return None
        
    def find_one_by_word_and_book_id(self, word: str, book_id: int) -> dict:
        word = None
        
        sql = f'SELECT * FROM word WHERE word = "{word}" AND book_id = {book_id}'
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        
        if result is not None:
            word = WordModel(id=result['id'], book_id=result['book_id'], word=result['word']
                         , mean=result['mean'], created_at=result['created_at'], updated_at=result['updated_at'])
        
        return word.__dict__
    
    def add(self, book_id: int, word: str, mean: str) -> dict:
        sql = f"INSERT INTO word (book_id, word, mean) VALUES ({book_id}, '{word}', '{mean}')"
        self.cursor.execute(sql)
        self.connect.commit()
        
        word = WordModel(id=self.cursor.lastrowid, book_id=book_id, word=word, mean=mean)
        
        return word.__dict__
    
    def update(self, id: int, book_id: int, word: str, mean: str) -> dict:
        sql = f"UPDATE word SET book_id={book_id}, word='{word}', mean='{mean}' WHERE id = {id}"
        self.cursor.execute(sql)
        self.connect.commit()
        
        word = WordModel(id=id, book_id=book_id, word=word, mean=mean)
        
        return word.__dict__
        
    def delete(self, id: int):
        sql = f"DELETE FROM word WHERE id={id}"
        self.cursor.execute(sql)
        self.connect.commit()

        return {'id': id}