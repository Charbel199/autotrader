import time
from datetime import datetime
import datetime as dt
import random


def from_binance_date_to_timestamp(date: str) -> int:
    try:
        timestamp = time.mktime(datetime.strptime(date, "%d %b, %Y").timetuple())
        return int(timestamp)
    except:
        raise ValueError(f"Couldn't convert {date} to timestamp.")


def from_timestamp_to_binance_date(timestamp: int) -> str:
    try:
        date = datetime.fromtimestamp(timestamp).strftime("%d %b %Y %H:%M ")
        return date
    except:
        raise ValueError(f"Couldn't convert {timestamp} to date.")


def get_previous_timestamp(timestamp: int, hours: int = 0, minutes: int = 0) -> int:
    try:
        if hours != 0:
            timestamp -= 3600 * hours
        if minutes != 0:
            timestamp -= 60 * minutes
        return timestamp
    except:
        raise ValueError(f"Couldn't get previous timestamp from {timestamp} going back {hours} hours and {minutes} minutes.")


def get_next_timestamp(timestamp: int, hours: int = 0, minutes: int = 0) -> int:
    try:
        if hours != 0:
            timestamp += 3600 * hours
        if minutes != 0:
            timestamp += 60 * minutes
        return timestamp
    except:
        raise ValueError(f"Couldn't get next timestamp from {timestamp} going forward {hours} hours and {minutes} minutes.")


def get_random_timestamp(lower_bound_timestamp: int, upper_bound_timestamp: int = None) -> int:
    if upper_bound_timestamp is None:
        upper_bound_timestamp = get_current_timestamp()
    if upper_bound_timestamp < lower_bound_timestamp:
        temp = upper_bound_timestamp
        upper_bound_timestamp = lower_bound_timestamp
        lower_bound_timestamp = temp
    return random.randint(lower_bound_timestamp, upper_bound_timestamp)


def from_timestamp_to_date(timestamp: int) -> str:
    try:
        date = datetime.fromtimestamp(timestamp).strftime("%d %b %Y %H:%M ")
        return date
    except:
        raise ValueError(f"Couldn't convert {timestamp} to date.")


def get_current_timestamp() -> int:
    return int(datetime.now(dt.timezone.utc).timestamp())


def from_seconds_to_time(seconds: int)->str:
    seconds_in_day = 60 * 60 * 24
    seconds_in_hour = 60 * 60
    seconds_in_minute = 60

    days = seconds // seconds_in_day
    hours = (seconds - (days * seconds_in_day)) // seconds_in_hour
    minutes = (seconds - (days * seconds_in_day) - (hours * seconds_in_hour)) // seconds_in_minute
    return f"{days} days, {hours} hours, {minutes} minutes"