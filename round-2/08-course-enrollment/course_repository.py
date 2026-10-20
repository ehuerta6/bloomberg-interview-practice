from collections import defaultdict
from course_models import Enrollment

class CourseRepository:
    def __init__(self):
        self.courses = {}
        self.enrollments = {}
        self.completions = defaultdict(set)

    def add_course(self, course_id, capacity, prerequisites=None):
        self.courses[course_id] = {"capacity": capacity, "prerequisites": set(prerequisites or ())}

    def course(self, course_id):
        return self.courses.get(course_id)

    def enrollment(self, enrollment_id):
        return self.enrollments.get(enrollment_id)

    def status(self, enrollment_id):
        row = self.enrollment(enrollment_id)
        return row.status if row else None

    def for_course(self, course_id):
        return [row for row in self.enrollments.values() if row.course_id == course_id]

    def enrolled_count(self, course_id):
        return sum(row.status == "enrolled" for row in self.for_course(course_id))

    def for_student_course(self, student_id, course_id):
        return next((row for row in self.for_course(course_id) if row.student_id == student_id and row.status in {"enrolled", "waitlisted"}), None)

    def add_enrollment(self, enrollment):
        self.enrollments[enrollment.enrollment_id] = enrollment

    def mark_complete(self, student_id, course_id):
        self.completions[student_id].add(course_id)

    def has_prerequisites(self, student_id, course_id):
        return self.course(course_id)["prerequisites"] <= self.completions[student_id]

    def promote_next(self, course_id):
        waiting = sorted((row for row in self.for_course(course_id) if row.status == "waitlisted"), key=lambda row: row.enrollment_id)
        if waiting and self.enrolled_count(course_id) < self.course(course_id)["capacity"]:
            waiting[0].status = "enrolled"
            return waiting[0]
        return None
