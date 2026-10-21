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

    def test_expired_owner_cannot_complete_after_reclaim(self):
        _, queue = self.build()
        queue.enqueue("job-4", "export", {})
        queue.claim("worker-a", 100)
        queue.claim("worker-b", 131)
        self.assertEqual(queue.complete("job-4", "worker-a", 132).status, "conflict")
        self.assertEqual(queue.complete("job-4", "worker-b", 132).status, "done")

    def test_expired_final_attempt_is_marked_failed(self):
        store = JobStore()
        queue = JobQueue(store, lease_seconds=5, max_attempts=1)
        queue.enqueue("job-5", "notify", {})
        queue.claim("worker-a", 10)
        self.assertIsNone(queue.claim("worker-b", 15))
        self.assertEqual(store.get("job-5").status, "failed")


    def test_wrong_worker_cannot_complete_active_lease(self):
        store, queue = self.build()
        queue.enqueue("job-4", "sync", {})
        queue.claim("worker-a", 100)
        self.assertEqual(queue.complete("job-4", "worker-b", 101).status, "conflict")
        self.assertEqual(store.get("job-4").status, "leased")


    def test_retry_limit_moves_job_to_terminal_failed_state(self):
        store, queue = self.build()
        queue.enqueue("job-5", "sync", {})
        queue.claim("worker-a", 100)
        queue.fail("job-5", "worker-a", "first", 101)
        queue.claim("worker-b", 102)
        queue.fail("job-5", "worker-b", "second", 103)
        queue.claim("worker-c", 104)
        self.assertEqual(queue.fail("job-5", "worker-c", "last", 105).status, "failed")
        self.assertIsNone(queue.claim("worker-d", 200))


    def test_lease_expiry_boundary_rejects_old_worker(self):
        store, queue = self.build()
        queue.enqueue("job-6", "sync", {})
        queue.claim("worker-a", 100)
        self.assertEqual(queue.complete("job-6", "worker-a", 130).status, "conflict")
        self.assertEqual(store.get("job-6").status, "leased")


    def test_duplicate_job_id_is_rejected(self):
        _, queue = self.build()
        queue.enqueue("job-7", "sync", {})
        with self.assertRaises(ValueError):
            queue.enqueue("job-7", "other", {})

if __name__ == "__main__":
    unittest.main()
