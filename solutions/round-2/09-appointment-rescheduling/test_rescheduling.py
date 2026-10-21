import unittest
from appointment_repository import AppointmentRepository
from appointment_service import AppointmentService

class RescheduleTests(unittest.TestCase):
    def setUp(self):
        self.repo = AppointmentRepository()
        self.repo.add_appointment("a1", "patient-a", "10:00")
        self.repo.add_appointment("a2", "patient-b", "11:00")
        self.service = AppointmentService(self.repo)

    def test_reschedule_moves_appointment_to_free_slot(self):
        self.assertEqual(self.service.reschedule("a1", "patient-a", "12:00"), "rescheduled")
        self.assertEqual(self.repo.time_of("a1"), "12:00")
        self.assertIsNone(self.repo.appointment_at("10:00"))

    def test_conflict_leaves_original_appointment_unchanged(self):
        self.assertEqual(self.service.reschedule("a1", "patient-a", "11:00"), "conflict")
        self.assertEqual(self.repo.time_of("a1"), "10:00")
        self.assertEqual(self.repo.appointment_at("10:00").appointment_id, "a1")
        self.assertEqual(self.repo.appointment_at("11:00").appointment_id, "a2")

    def test_only_owner_can_reschedule(self):
        self.assertEqual(self.service.reschedule("a1", "patient-b", "12:00"), "not_found")
        self.assertEqual(self.repo.time_of("a1"), "10:00")

    def test_unknown_appointment_does_not_change_schedule(self):
        self.assertEqual(self.service.reschedule("missing", "patient-a", "12:00"), "not_found")
        self.assertIsNone(self.repo.appointment_at("12:00"))

    def test_rescheduling_to_same_slot_is_successful(self):
        self.assertEqual(self.service.reschedule("a1", "patient-a", "10:00"), "rescheduled")
        self.assertEqual(self.repo.time_of("a1"), "10:00")

    def test_empty_new_slot_is_rejected_without_moving_appointment(self):
        self.assertEqual(self.service.reschedule("a1", "patient-a", ""), "not_found")
        self.assertEqual(self.repo.time_of("a1"), "10:00")


    def test_failed_second_move_rolls_back_to_current_slot(self):
        self.service.reschedule("a1", "patient-a", "12:00")
        self.assertEqual(self.service.reschedule("a1", "patient-a", "11:00"), "conflict")
        self.assertEqual(self.repo.time_of("a1"), "12:00")
        self.assertIsNone(self.repo.appointment_at("10:00"))

if __name__ == "__main__": unittest.main()
