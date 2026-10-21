import unittest

from delivery_service import DeliveryService
from delivery_store import DeliveryStore
from notification_provider import RecordingProvider


class NotificationDeliveryTests(unittest.TestCase):
    def build(self, outcomes=None):
        store = DeliveryStore()
        provider = RecordingProvider(outcomes or [])
        return store, provider, DeliveryService(store, provider, max_attempts=3)

    def test_success_is_recorded_and_replay_is_deduplicated(self):
        store, provider, service = self.build()
        first = service.deliver("evt-1", "riley", "Your report is ready")
        second = service.deliver("evt-1", "riley", "Your report is ready")
        self.assertEqual(first.status, "sent")
        self.assertEqual(second.status, "sent")
        self.assertEqual(provider.calls, 1)
        self.assertEqual(store.get("evt-1").attempts, 1)

    def test_transient_failures_retry_and_eventually_persist_success(self):
        store, provider, service = self.build([False, False, True])
        result = service.deliver("evt-2", "sam", "Build finished")
        self.assertEqual(result.status, "sent")
        self.assertEqual(provider.calls, 3)
        self.assertEqual(store.get("evt-2").attempts, 3)

    def test_exhausted_retries_remain_failed_and_can_be_retried_later(self):
        store, provider, service = self.build([False, False, False, True])
        failed = service.deliver("evt-3", "lee", "Payment received")
        self.assertEqual(failed.status, "failed")
        self.assertEqual(store.get("evt-3").attempts, 3)
        retried = service.retry("evt-3")
        self.assertEqual(retried.status, "sent")
        self.assertEqual(store.get("evt-3").attempts, 4)


    def test_event_key_cannot_be_reused_for_different_content(self):
        store, provider, service = self.build()
        service.deliver("evt-4", "riley", "first")
        with self.assertRaises(ValueError):
            service.deliver("evt-4", "riley", "changed")
        self.assertEqual(provider.calls, 1)


    def test_retry_after_success_does_not_call_provider_again(self):
        _, provider, service = self.build()
        service.deliver("evt-5", "riley", "ready")
        self.assertEqual(service.retry("evt-5").status, "sent")
        self.assertEqual(provider.calls, 1)


    def test_exhausted_failure_is_persisted_before_later_retry(self):
        store, _, service = self.build([False, False, False, True])
        self.assertEqual(service.deliver("evt-6", "riley", "ready").status, "failed")
        self.assertEqual(store.get("evt-6").attempts, 3)
        self.assertEqual(service.retry("evt-6").status, "sent")

if __name__ == "__main__":
    unittest.main()
