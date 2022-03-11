from datetime import datetime, timedelta
import pytz
import time


def get_next_billing_time(type_of_subs: int) -> int:
    timezone = pytz.timezone("Asia/Ho_Chi_Minh")
    last_day = datetime.now(tz=timezone) - timedelta(days=1)
    end_of_today_last_day = datetime(
        year=last_day.year,
        month=last_day.month,
        day=last_day.day,
        hour=23,
        minute=59,
        second=59,
        tzinfo=timezone
    )
    next_billing_day = end_of_today_last_day + timedelta(days=type_of_subs)

    return int(time.mktime(next_billing_day.timetuple()))


def get_current_time():
    timezone = pytz.timezone("Asia/Ho_Chi_Minh")

    return int(time.mktime(datetime.now(timezone).timetuple()))
