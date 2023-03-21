import re


def validate_email(email):
    email_validation = re.compile("^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    if email_validation.match(email):
        return True
    return False

# 8자 이상, 하나 이상의 숫자, 하나 이상의 문자, 하나 이상의 특수문자
def validate_password(password):
    password_validation = re.compile("^.*(?=^.{8,}$)(?=.*\d)(?=.*[a-zA-Z])(?=.*[!@#$%*^&+=]).*$")
    if password_validation.match(password):
        return True
    return False

def validate_word(word, mean):
    if len(word) <= 15 and len(mean) <= 15:
        return word.strip(), mean.strip()
    return False