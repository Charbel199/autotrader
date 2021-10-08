import time
from datetime import datetime
import datetime as dt

def from_binance_date_to_timestamp(date):
    try:
        timestamp = time.mktime(datetime.strptime(date, "%d %b, %Y").timetuple())
        return int(timestamp)
    except:
        return


def from_timestamp_to_binance_date(timestamp):
    try:
        date = datetime.fromtimestamp(timestamp).strftime("%d %b, %Y")
        return date
    except:
        return


def from_timestamp_to_date(timestamp):
    try:
        date = datetime.fromtimestamp(timestamp).strftime("%d %b %Y %H:%M ")
        return date
    except:
        return


def get_current_timestamp():
    return int(datetime.now(dt.timezone.utc).timestamp())

