import time
from datetime import datetime
import datetime as dt
import random


def from_binance_date_to_timestamp(date):
    try:
        timestamp = time.mktime(datetime.strptime(date, "%d %b, %Y").timetuple())
        return int(timestamp)
    except:
        return


def from_timestamp_to_binance_date(timestamp):
    try:
        date = datetime.fromtimestamp(timestamp).strftime("%d %b %Y %H:%M ")
        return date
    except:
        return


def get_previous_timestamp(timestamp, hours=0, minutes=0):
    try:
        if hours != 0:
            timestamp -= 3600 * hours
        if minutes != 0:
            timestamp -= 60 * minutes
        return timestamp
    except:
        return


def get_next_timestamp(timestamp, hours=0, minutes=0):
    try:
        if hours != 0:
            timestamp += 3600 * hours
        if minutes != 0:
            timestamp += 60 * minutes
        return timestamp
    except:
        return


def get_random_timestamp(lower_bound_timestamp, upper_bound_timestamp=None):
    if upper_bound_timestamp is None:
        upper_bound_timestamp = get_current_timestamp()
    return random.randint(lower_bound_timestamp, upper_bound_timestamp)


def from_timestamp_to_date(timestamp):
    try:
        date = datetime.fromtimestamp(timestamp).strftime("%d %b %Y %H:%M ")
        return date
    except:
        return


def get_current_timestamp():
    return int(datetime.now(dt.timezone.utc).timestamp())
