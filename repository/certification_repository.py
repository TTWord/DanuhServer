from db.connect import Connect
from datetime import datetime


class CertificationRepository(Connect):
    def add(self, certification_info: dict) -> dict:
        sql = f"""
            INSERT INTO certification (
                cert_type, cert_key, cert_code, expired_time
            )
            VALUES(
                '{certification_info['cert_type']}',
                '{certification_info['cert_key']}',
                '{certification_info['cert_code']}',
                '{certification_info['expired_time']}'
            );
        """
        self.cursor.execute(sql)
        self.connect.commit()

        return {'verification_id': certification_info["cert_code"]}
    
    def find_one_by_cert_key(self, cert_key: str) -> dict:
        sql = f'SELECT * FROM certification WHERE cert_key = "{cert_key}";'
        self.cursor.execute(sql)
        certification = self.cursor.fetchone()
        
        return certification
    
    def update(self, cert_key: str, cert_code: str, expired_time: str) -> dict:
        sql = f"UPDATE certification SET cert_code = '{cert_code}', expired_time = '{expired_time}' WHERE cert_key = '{cert_key}'"

        self.cursor.execute(sql)
        self.connect.commit()

        return {'verification_id': cert_code}