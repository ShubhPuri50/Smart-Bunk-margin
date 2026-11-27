from .student import Student
from .subject import SubjectAttendance


class AttendancePlanner:
    def __init__(self, student):
        if not isinstance(student, Student):
            raise TypeError("student must be a Student")
        self.student = student
        self.subject_records = student.subject_records

    def add_subject(self, subject_name, attended, conducted, required_percentage):
        record = SubjectAttendance(
            subject_name, attended, conducted, required_percentage
        )
        self.subject_records.append(record)
        return record

    def analyze_subject(self, subject_name):
        name = str(subject_name).strip().lower()
        for record in self.subject_records:
            if record.subject_name.lower() == name:
                return record
        return None

    def generate_report(self):
        return "\n".join(
            f"{record.subject_name}: {record.calculate_percentage():.2f}% "
            f"({record.classify_risk()})"
            for record in self.subject_records
        )
