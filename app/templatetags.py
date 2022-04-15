from humanize.time import precisedelta, naturaltime, naturaldate
from datetime import datetime, timedelta

from app import app


@app.template_filter('humanize_time')
def humanize_time(value):
    """
    Returns the timedelta between `value` and now in a human-friendly format
    """
    if value:
        now = datetime.now()
        delta = now - value
        if delta < timedelta(hours=1):
            return naturaltime(delta, minimum_unit='seconds')
        else:
            return f"{naturaldate(value)} at {value.strftime('%H:%M')}"
    else:
        return ""
