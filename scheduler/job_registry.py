class JobRegistry:
    def __init__(self):
        self.jobs = {}

    def add_job(self, job):
        self.jobs[job.job_id] = job

    def remove_job(self, job_id):
        if job_id in self.jobs:
            del self.jobs[job_id]

    def get_all_jobs(self):
        return self.jobs.values()