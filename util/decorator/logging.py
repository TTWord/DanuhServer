from flask import current_app as app
from functools import wraps


def logging(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        messages = func(*args, **kwargs)
        if messages.status_code==200:
            pass
        else:
            app.logger.warning("{}: {}".format(messages.status_code, messages.status))
        return messages
    return wrapper