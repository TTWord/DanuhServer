# TODO: 메일 인증
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from email.mime.base import MIMEBase
# from email import encoders

# smtp = smtplib.SMTP('smtp.gmail.com', 587)
# smtp.ehlo()      # say Hello    smtp에서 리턴 발생 smtp서버가 불안정한 경우 에러 발생
# smtp.starttls()  # TLS(Transfortation Layer Secret) 전송간 암호화 전송, 사용시 필요 전송레이어암호화
# # 암호 보호를 위해 os.environ로 환경변수를 통해서 받아오기도 한다.
# smtp.login('kimjunghyun696', 'clzlstughcvjomtv')

# # message 
# msg = MIMEMultipart()
# msg['Subject'] = 'test'

# # 내용은 text뿐 아닌 html도 가능
# report_file = open("etc/mail/email.html", encoding="utf-8")
# html = """\
# <!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <meta http-equiv="X-UA-Compatible" content="IE=edge">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <title>이메일 인증</title>
#     <!--<link rel="stylesheet" href="reset.css">-->
#     <style>
#         @font-face {
#             font-family: 'GmarketSansMedium';
#             src: url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_2001@1.1/GmarketSansMedium.woff') format('woff');
#             font-weight: normal;
#             font-style: normal;
#         }
#         .wrapper {
#             width: 1213px;
#             height: 852px;
#             display: flex;
#             justify-content: center;
#             align-items: center;
#         }
#         .email--wrapper {
#             width: 1051px;
#             height: 656px;
#             display: flex;
#             justify-content: center;
#             align-items: center;
#         }
#         .content--wrapper {
#             width: 337px;
#             height: 287px;
#             display: flex;
#             flex-direction: column;
#             justify-content: space-between;
#             align-items: center;
#         }
#         span {
#             font-size: 64px;
#             font-weight: bold;
#             color: white;
#             font-family: 'GmarketSansMedium';
#         }
#         div {
#             font-family: 'GmarketSansMedium';
#         }
#     </style>
# </head>
# <body>
#     <div class="wrapper">
#         <div class="email--wrapper">
#             <div class="content--wrapper">
#                 <img style="width: 243px; height: 64px;" src=asfasfasfasf alt="TTWord-Logo">
#                 <div style="font-size: 16px; color: #5C369A;">웹 / 앱에서 이메일 인증코드를 입력해주세요</div>
#                 <div style="font-weight: bold; font-size: 24px; color: #5C369A;">이메일 인증코드</div>
#                 <div style="width: 337px; height: 130px; background: linear-gradient(180deg, #6111E2 0%, #481896 100%);
#                 box-shadow: 0px 0px 8px rgba(143, 51, 186, 0.5);
#                 border-radius: 18px; display: flex; justify-content:center; align-items: center;">
#                     <div style="width: 260px; height: 64px; display: flex; justify-content:space-between; align-items: center;">
#                         <span>132</span>
#                         <span>032</span>
#                     </div>
#                 </div>
#             </div>
#         </div>
#     </div>
# </body>
# </html>
# """
# #alert_msg = MIMEText(report_file.read(),"html", "utf-8")
# content = MIMEText(html, "html")
# msg.attach(content)

# # 첨부파일
# # filepath = "./png/1.png"
# # with open(filepath, "rb") as f:
# #     # octet-stream : 메모리에 한번에 다 올리는 것이 아닌 버퍼 사이즈만큼 올리는 것
# #     file = MIMEBase("application", "octet-stream")
# #     # chunk로 나눠서 보내는 것
# #     file.set_payload(f.read())
# #     # base64로 인코딩 이미지 파일을 서버에 올릴때 멀티파트로 올리는 것이 아닌 string으로 올린다
# #     encoders.encode_base64(file)
# #     # 첨부파일 이름 ? 이미지인경우 추가하여 이미지 밑에 내용이 나타나게 됨. 
# #     file.add_header('Content-Disposition', 'attachment', filename=filepath)
# #     msg.attach(file)

# # 메일 보내기
# addr = "djsk721@naver.com"
# msg["To"] = addr
# smtp.sendmail("kimjunghyun696@gmail.com", addr, msg.as_string())
# smtp.quit()