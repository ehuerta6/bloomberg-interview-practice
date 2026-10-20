class AppointmentService:
    def __init__(self, repository):
        self.repository = repository

    def reschedule(self, appointment_id, patient_id, new_time):
        appointment = self.repository.appointment(appointment_id)
        if appointment is None or appointment.patient_id != patient_id or not new_time:
            return "not_found"
        original_time = appointment.time
        self.repository.move(appointment_id, new_time)
        conflict = self.repository.appointment_at(new_time, exclude_id=appointment_id)
        if conflict is not None:
            self.repository.move(appointment_id, original_time)
            return "conflict"
        return "rescheduled"
