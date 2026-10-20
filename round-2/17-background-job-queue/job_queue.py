from job import Job


class JobQueue:
    def __init__(self, store, lease_seconds=30, max_attempts=3):
        self.store, self.lease_seconds, self.max_attempts = store, lease_seconds, max_attempts

    def enqueue(self, job_id, kind, payload):
        self.store.add(Job(job_id, kind, dict(payload)))

    def claim(self, worker, now):
        for job in self.store.pending():
            if job.status == "done" or job.attempts >= self.max_attempts:
                continue
            job.status = "leased"
            job.lease_owner = worker
            job.lease_until = now + self.lease_seconds
            job.attempts += 1
            return job
        return None

    def complete(self, job_id, worker, now):
        job = self.store.get(job_id)
        if job is None:
            return type("Result", (), {"status": "missing"})()
        if job.status == "done":
            return type("Result", (), {"status": "done"})()
        if job.status != "leased" or job.lease_owner != worker or job.lease_until < now:
            return type("Result", (), {"status": "conflict"})()
        job.status, job.lease_owner = "done", None
        return type("Result", (), {"status": "done"})()

    def fail(self, job_id, worker, error, now):
        job = self.store.get(job_id)
        if job is None or job.status != "leased" or job.lease_owner != worker or job.lease_until < now:
            return type("Result", (), {"status": "conflict"})()
        job.last_error, job.lease_owner = error, None
        job.status = "failed" if job.attempts >= self.max_attempts else "queued"
        return type("Result", (), {"status": job.status})()
