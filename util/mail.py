import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import config


class EmailSender:
    @staticmethod
    def send_email(from_email, to_email, subject, body):
        try:
            smtp_server = config['SMTP_SERVER']
            smtp_port = config['SMTP_PORT']
            smtp_username = config['SMTP_USERNAME']
            smtp_password = config['SMTP_PASSWORD']
            stml_html = config['STML_HTML']

            msg = MIMEMultipart()
            msg['From'] = from_email
            msg['To'] = to_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            html = open(stml_html, encoding='utf-8').read()
            msg.attach(MIMEText(html, 'html'))

            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(smtp_username, smtp_password)
                server.sendmail(from_email, to_email, msg.as_string())
        except smtplib.SMTPAuthenticationError:
            return {'message': "Could not authenticate with the SMTP server."}, 401 
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