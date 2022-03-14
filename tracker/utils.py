from datetime import datetime

import pytz


def get_local_timestamp(timestamp=None):
    timezone = pytz.timezone('Asia/Kathmandu')
    if not timestamp:
        timestamp = datetime.now(timezone)
    else:
        timestamp = timestamp.astimezone(timezone)
    formatted_timestamp = timestamp.strftime('%d %B %Y %H:%M:%S')
    return formatted_timestamp


get_local_timestamp()
