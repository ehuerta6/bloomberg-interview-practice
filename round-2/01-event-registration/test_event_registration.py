import unittest
from event_models import Event
from event_repository import EventRepository
from registration_routes import RegistrationRoutes
from registration_service import RegistrationService


class RegistrationTests(unittest.TestCase):
    def setUp(self):
        self.repo = EventRepository()
        self.repo.add_event(Event("career-night", 1))
        self.registration_routes = RegistrationRoutes(RegistrationService(self.repo))

    def register(self, student, registration):
        return self.registration_routes.post_registration({"event_id": "career-night", "student_id": student, "registration_id": registration})

    def test_capacity_blocks_second_active_student(self):
        self.assertEqual(self.register("s1", "r1")["status"], 201)
        self.assertEqual(self.register("s2", "r2")["status"], 409)

    def test_cancelled_registration_frees_capacity(self):
        self.register("s1", "r1")
        self.registration_routes.delete_registration("r1")
        self.assertEqual(self.register("s2", "r2")["status"], 201)

    def test_duplicate_active_registration_is_rejected(self):
        self.register("s1", "r1")
        self.assertEqual(self.register("s1", "r2")["status"], 409)

    def test_unknown_cancellation_preserves_active_registration(self):
        self.assertEqual(self.register("s1", "r1")["status"], 201)
        self.assertEqual(self.registration_routes.delete_registration("missing")["status"], 404)
        self.assertEqual(self.repo.get_registration("r1").status, "active")
        self.assertEqual(len(self.repo.active_for_student("career-night", "s1")), 1)


if __name__ == "__main__":
    unittest.main()
