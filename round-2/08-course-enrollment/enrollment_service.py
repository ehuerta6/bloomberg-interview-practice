from course_models import Enrollment

class EnrollmentService:
    def __init__(self, repository):
        self.repository = repository

    def enroll(self, student_id, course_id, enrollment_id):
        course = self.repository.course(course_id)
        if not course or not student_id or not enrollment_id or self.repository.enrollment(enrollment_id):
            return "rejected"
        if self.repository.for_student_course(student_id, course_id):
            return "duplicate"
        status = "enrolled" if self.repository.enrolled_count(course_id) < course["capacity"] else "waitlisted"
        self.repository.add_enrollment(Enrollment(enrollment_id, student_id, course_id, status))
        return status

    def drop(self, enrollment_id):
        enrollment = self.repository.enrollment(enrollment_id)
        if enrollment is None or enrollment.status not in {"enrolled", "waitlisted"}:
            return False
        enrollment.status = "dropped"
        self.repository.promote_next(enrollment.course_id)
        return True
