from dataclasses import dataclass

@dataclass
class Enrollment:
    enrollment_id: str
    student_id: str
    course_id: str
    status: str
