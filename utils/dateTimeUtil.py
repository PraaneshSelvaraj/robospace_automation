from datetime import datetime
import pytz

def get_current_ist_time() -> str:
    return datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')