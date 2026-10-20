import unittest

from job_queue import JobQueue
from job_store import JobStore


class BackgroundJobQueueTests(unittest.TestCase):
    def build(self):
        store = JobStore()
        return store, JobQueue(store, lease_seconds=30, max_attempts=3)

    def test_claim_assigns_lease_and_prevents_concurrent_claim(self):
        store, queue = self.build()
        queue.enqueue("job-1", "send_digest", {"user": "riley"})
        first = queue.claim("worker-a", 100)
        second = queue.claim("worker-b", 100)
        self.assertEqual(first.id, "job-1")
        self.assertEqual(second, None)
        self.assertEqual(store.get("job-1").lease_owner, "worker-a")

    def test_expired_lease_can_be_reclaimed_without_losing_attempt_history(self):
        store, queue = self.build()
        queue.enqueue("job-2", "resize_image", {"key": "x"})
        queue.claim("worker-a", 100)
        reclaimed = queue.claim("worker-b", 131)
        self.assertEqual(reclaimed.lease_owner, "worker-b")
        self.assertEqual(store.get("job-2").attempts, 2)

    def test_retry_and_duplicate_completion_do_not_run_job_twice(self):
        store, queue = self.build()
        queue.enqueue("job-3", "sync", {})
        job = queue.claim("worker-a", 100)
        self.assertEqual(queue.fail("job-3", "worker-a", "temporary", 101).status, "queued")
        retried = queue.claim("worker-b", 102)
        self.assertEqual(queue.complete("job-3", "worker-b", 103).status, "done")
        self.assertEqual(queue.complete("job-3", "worker-b", 104).status, "done")
        self.assertEqual(store.get("job-3").attempts, 2)


if __name__ == "__main__":
    unittest.main()
