class JobStore:
    def __init__(self):
        self.jobs = {}

    def add(self, job):
        if job.id in self.jobs:
            raise ValueError("duplicate job id")
        self.jobs[job.id] = job

    def get(self, job_id):
        return self.jobs.get(job_id)

    def pending(self):
        return list(self.jobs.values())
