from util.passwordEncryption import encrypt_password, compare_passwords

# TODO : Model_info 클래스 객체
#      : model 폴더에 생성
class UserRepository:    
    def signup(self, user_info):        
        with self.cursor as cursor:
            # sql = """
            #     SELECT * FROM user
            # """
            sql = f"""
                INSERT INTO user (
                    username, password, nickname
                )
                VALUES(
                    {user_info['username']},
                    {user_info['password']},
                    {user_info['nickname']}
                )
            """
            cursor.execute(sql)
            cursor.commit()

    def find_user(self):
        with self.cursor as cursor:
            sql = 'SELECT * FROM user'
            cursor.execute(sql)
            result = cursor.fetchall()
            print("결과: ", result)
        
        return 0