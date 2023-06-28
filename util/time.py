from datetime import datetime


def get_difference_time(t):
    time_difference = datetime.now() - t

    # Extract the days, hours, and minutes from the time difference
    days = time_difference.days
    hours = time_difference.seconds // 3600
    minutes = (time_difference.seconds // 60) % 60
    if days > 0:
        time_ago = f"{days}일 전"
    elif hours > 0:
        time_ago = f"{hours}시간 전"
    else:
        time_ago = f"{minutes}분 전"

    return time_ago