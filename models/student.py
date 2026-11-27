class Student:
    def __init__(self, student_id, name):
        if not str(student_id).strip():
            raise ValueError("student ID cannot be empty")
        if not str(name).strip():
            raise ValueError("student name cannot be empty")
        self.student_id = str(student_id).strip()
        self.name = str(name).strip()
        self.subject_records = []

    def add_subject(self, subject):
        self.subject_records.append(subject)

    def view_records(self):
        return list(self.subject_records)
