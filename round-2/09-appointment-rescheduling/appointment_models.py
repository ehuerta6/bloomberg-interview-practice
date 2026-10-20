from dataclasses import dataclass

@dataclass
class Appointment:
    appointment_id: str
    patient_id: str
    time: str
