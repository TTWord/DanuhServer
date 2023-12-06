from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from util.custom_response import custom_response
from flask_limiter import Limiter


# Setup the Rate Limiter
limiter = Limiter(
    get_remote_address,
    storage_uri="memory://",

)

# Custom decorator to handle rate limiting errors for a specific endpoint
def handle_rate_limit_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return custom_response("TOO_MANY_REQUESTS", code=429)
    return wrapper
