from datetime import datetime
import pytz

def get_current_ist_time(string=True):
    return datetime.now(pytz.timezone('Asia/Kolkata'))
