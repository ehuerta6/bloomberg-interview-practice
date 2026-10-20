import unittest
from course_repository import CourseRepository
from enrollment_service import EnrollmentService

class EnrollmentTests(unittest.TestCase):
    def setUp(self):
        self.repo = CourseRepository()
        self.repo.add_course("intro", 2)
        self.repo.add_course("advanced", 1, prerequisites={"intro"})
        self.service = EnrollmentService(self.repo)

    def test_prerequisite_is_required_before_enrollment(self):
        self.assertEqual(self.service.enroll("s1", "advanced", "e1"), "prerequisite_missing")
        self.assertEqual(self.repo.status("e1"), None)

    def test_completed_prerequisite_allows_advanced_enrollment(self):
        self.repo.mark_complete("s1", "intro")
        self.assertEqual(self.service.enroll("s1", "advanced", "e1"), "enrolled")

    def test_enrollment_consumes_capacity_and_next_student_waitlists(self):
        self.assertEqual(self.service.enroll("s1", "intro", "e1"), "enrolled")
        self.assertEqual(self.service.enroll("s2", "intro", "e2"), "enrolled")
        self.assertEqual(self.service.enroll("s3", "intro", "e3"), "waitlisted")
        self.assertEqual(self.repo.enrolled_count("intro"), 2)

    def test_waitlist_does_not_consume_capacity_after_drop(self):
        self.service.enroll("s1", "intro", "e1")
        self.service.enroll("s2", "intro", "e2")
        self.service.enroll("s3", "intro", "e3")
        self.assertTrue(self.service.drop("e1"))
        self.assertEqual(self.repo.status("e3"), "enrolled")
        self.assertEqual(self.repo.enrolled_count("intro"), 2)

    def test_duplicate_enrollment_is_rejected(self):
        self.service.enroll("s1", "intro", "e1")
        self.assertEqual(self.service.enroll("s1", "intro", "e2"), "duplicate")

    def test_drop_is_single_use_and_releases_capacity(self):
        self.service.enroll("s1", "intro", "e1")
        self.assertTrue(self.service.drop("e1"))
        self.assertFalse(self.service.drop("e1"))
        self.assertEqual(self.repo.status("e1"), "dropped")

if __name__ == "__main__": unittest.main()
