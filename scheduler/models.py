from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass
class ScrapeJob:
    job_id: str
    scraper_type: str
    target_url: str
    query: str
    frequency: str
    start_time: str
    start_date: str
    export_format: str
    max_rows: int
    email_notification: bool
    is_active: bool
    start_minute: int = 0
    created_at: datetime = field(default_factory=datetime.now)