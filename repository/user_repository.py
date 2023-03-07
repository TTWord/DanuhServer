from db.connect import Connect


class UserRepository(Connect): 
    def add(self, user_info: dict) -> dict:
        sql = f"""
            INSERT INTO user (
                username, password, nickname
            )
            VALUES(
                '{user_info['username']}',
                '{user_info['password']}',
                '{user_info['nickname']}'
            );
        """
        self.cursor.execute(sql)
        self.connect.commit()

    def delete(self, user_id: str) -> dict:
        sql = f"DELETE FROM user WHERE username = '{user_id}'"
        self.cursor.execute(sql)
        self.connect.commit()
        return {'id': id}
    
    def find_one_by_username(self, user_id: str) -> dict:
        sql = f'SELECT * FROM user where username = "{user_id}"'
        self.cursor.execute(sql)
        user = self.cursor.fetchone()
        
        return user
    
    def find_one_by_user_id(self, id: int) -> dict:
        sql = f'SELECT * FROM user where id = "{id}"'
        self.cursor.execute(sql)
        user = self.cursor.fetchone()
        
        return user
    
    # TODO: Auth 관련(refectoring 필요)
    #     : Certification 테이블에 저장된 id를 이용해 인증 메일을 확인.
    #     : 추후 확장성 고려하여 Phone, Email, Kakao, Naver 등등 인증 추가
    #     : service/mail_service, repository/mail_repository or
    #     : service/certification_service, repository/certification_repository
    #     : 클래스 생성해서 인증 메일을 보내는 것으로 생각됨.
    def auth_add(self, verification_info: dict) -> dict:
        sql = f"""
            INSERT INTO certification (
                cert_type, cert_key, cert_code, expired_time
            )
            VALUES(
                '{verification_info['cert_type']}',
                '{verification_info['cert_key']}',
                '{verification_info['cert_code']}',
                '{verification_info['expired_time']}'
            );
        """
        self.cursor.execute(sql)
        self.connect.commit()

        return {'verification_id': verification_info["cert_code"]}
    
    def auth_find_one_by_cert_key(self, cert_key: str) -> dict:
        sql = f'SELECT * FROM certification WHERE cert_key = "{cert_key}";'
        self.cursor.execute(sql)
        certification = self.cursor.fetchone()
        
        return certification
    
    def auth_update(self, cert_key: str, cert_code: str) -> dict:
        sql = f"UPDATE certification SET cert_code = '{cert_code}' WHERE cert_key = '{cert_key}'"
        self.cursor.execute(sql)
        self.connect.commit()

        return {'verification_id': cert_code}