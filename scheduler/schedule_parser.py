from datetime import datetime
from typing import Optional
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger


def parse_schedule(frequency: str, start_time: str, start_minute: Optional[int] = None):
    hour, minute = map(int, start_time.split(":"))

    # If caller provided an explicit minute override (e.g., for hourly runs), use it
    minute_to_use = minute if start_minute is None else int(start_minute)

    if frequency == "Hourly":
        # If a minute is specified, run every hour at that minute; otherwise run every hour from now
        if start_minute is not None:
            return CronTrigger(minute=minute_to_use)
        return IntervalTrigger(hours=1)

    elif frequency == "Every 6h":
        # Repeat every 6 hours at the selected minute
        if start_minute is not None:
            return CronTrigger(hour="*/6", minute=minute_to_use)
        return IntervalTrigger(hours=6)

    elif frequency == "Daily":
        return CronTrigger(hour=hour, minute=minute_to_use)

    elif frequency == "Weekly":
        return CronTrigger(day_of_week='mon', hour=hour, minute=minute_to_use)

    elif frequency == "Monthly":
        return CronTrigger(day=1, hour=hour, minute=minute_to_use)

    else:
        raise ValueError("Unsupported frequency")