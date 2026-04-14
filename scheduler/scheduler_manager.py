from apscheduler.schedulers.background import BackgroundScheduler
from .schedule_parser import parse_schedule
from .job_executor import execute_job


class SchedulerManager:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()

    def add_job(self, job):
        trigger = parse_schedule(job.frequency, job.start_time, getattr(job, "start_minute", None))

        self.scheduler.add_job(
            execute_job,
            trigger=trigger,
            args=[job],
            id=job.job_id,
            replace_existing=True
        )

        print(f"✅ Job scheduled: {job.job_id}")

    def remove_job(self, job_id):
        self.scheduler.remove_job(job_id)

    def shutdown(self):
        self.scheduler.shutdown()