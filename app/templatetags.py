from humanize.time import naturaltime, naturaldate
from datetime import datetime, timedelta, timezone

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
            # This is a dirty hack, that works because we know the server is in UTC
            localized = value.replace(tzinfo=timezone.utc).astimezone(tz=None)
            return f"{naturaldate(localized)} at {localized.strftime('%H:%M')}"
    else:
        return ""
