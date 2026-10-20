from appointment_models import Appointment

class AppointmentRepository:
    def __init__(self):
        self.appointments = {}

    def add_appointment(self, appointment_id, patient_id, time):
        self.appointments[appointment_id] = Appointment(appointment_id, patient_id, time)

    def appointment(self, appointment_id):
        return self.appointments.get(appointment_id)

    def time_of(self, appointment_id):
        row = self.appointment(appointment_id)
        return row.time if row else None

    def appointment_at(self, time, exclude_id=None):
        return next((row for row in self.appointments.values() if row.time == time and row.appointment_id != exclude_id), None)

    def move(self, appointment_id, time):
        self.appointments[appointment_id].time = time
