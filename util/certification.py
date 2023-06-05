import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import config
import requests


class EmailSender:
    @staticmethod
    def send_email(to_email, subject, body, verification_id):
        try:
            smtp_server = config['SMTP_SERVER']
            smtp_port = config['SMTP_PORT']
            smtp_username = config['SMTP_USERNAME']
            smtp_password = config['SMTP_PASSWORD']
            stml_html = config['STML_HTML']

            msg = MIMEMultipart()
            msg['from'] = smtp_username
            msg['To'] = to_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            html = open(stml_html, encoding='utf-8').read()
            html = html.replace("verification", f"{verification_id}")
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
            return {'message': "An SMTP exception occurred."}, 409
        except Exception as e:
            return {'message': f"An exception occurred: {e}"}, 409
        else:
            return {"message": "Email sent successfully."}, 200


class OAuth:
    def __init__(self, service):
        self.service = service
        if self.service == "kakao":
            self.auth_server = "https://kauth.kakao.com%s"
            self.api_server = "https://kapi.kakao.com%s"
            self.auth_url = self.auth_server % "/oauth/token"
            self.user_url = self.api_server % "/v2/user/me"
        elif self.service == "google":
            self.auth_server = "https://oauth2.googleapis.com/%s"
            self.api_server = "https://oauth2.googleapis.com/%s"
            self.auth_url= self.auth_server % "/token"
            self.user_url = " https://www.googleapis.com/oauth2/v2/userinfo"
        elif self.service == "apple":
            self.auth_server = "https://appleid.apple.com/%s"
            self.api_server = "https://appleid.apple.com/%s"
            self.auth_url= self.auth_server % "/auth/token"
            self.user_url = self.auth_server % "/auth/authorize"

        self.default_header = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Cache-Control": "no-cache",
        }

    def auth(self, code):
        service = self.service.upper()
        return requests.post(
            url=self.auth_url,
            headers=self.default_header,
            data={
                "grant_type": "authorization_code",
                "client_id": config[f'{service}_CLIENT_ID'],
                "client_secret": config[f'{service}_CLIENT_SECRET'],
                "redirect_uri": config['REDIRECT_URI'] + "/" + self.service,
                "code": code,
            },
        ).json()
    
    def userinfo(self, bearer_token):        
        return requests.get(
            url=self.user_url,
            headers={
                "Authorization": bearer_token
            }
        ).json()