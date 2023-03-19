import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import config
import random


#   TODO: Authorization을 추가적으로 구현할 듯 ex) 핸드폰인증, Kakaotalk 인증 등등
class EmailSender:
    @staticmethod
    def send_email(to_email, subject, body, verification_id):
        try:
            smtp_server = config['SMTP_SERVER']
            smtp_port = config['SMTP_PORT']
            smtp_username = config['SMTP_USERNAME']
            smtp_password = config['SMTP_PASSWORD']
            stml_html = config['STML_HTML']

            verification_code_1, verification_code_2 = verification_id[0:3], verification_id[3:]

            msg = MIMEMultipart()
            msg['from'] = smtp_username
            msg['To'] = to_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            html = open(stml_html, encoding='utf-8').read()
            html = html.replace("<span>input1</span>", f"<span>{verification_code_1}</span>")
            html = html.replace("<span>input2</span>", f"<span>{verification_code_2}</span>")
            msg.attach(MIMEText(html, 'html'))

            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(smtp_username, smtp_password)
                server.sendmail(smtp_username, to_email, msg.as_string())
        except smtplib.SMTPAuthenticationError:
            return {'message': "Could not authenticate with the SMTP server."}, 502  
        except smtplib.SMTPConnectError:
            return {'message': "Could not connect to the SMTP server."}, 503
        except smtplib.SMTPDataError:
            return {'message': "An error occurred while sending the email data."}, 503
        except smtplib.SMTPException:
            return {'message': "An SMTP exception occurred."}, 404
        except Exception as e:
            return {'message': f"An exception occurred: {e}"}, 404
        else:
            return {"message": "Email sent successfully."}, 200