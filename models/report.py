class BaseReport:
    def __init__(self, title):
        self.title = title

    def generate_header(self):
        return f"===== {self.title} ====="


class AttendanceReport(BaseReport):
    def __init__(self, title, records):
        super().__init__(title)
        self.records = records

    def generate_summary(self):
        lines = [self.generate_header()]
        for record in self.records:
            lines.append(
                f"{record['subject']} | {record['attended']}/{record['conducted']} "
                f"| {record['_percentage']:.2f}% | {record['_risk']}"
            )
        return "\n".join(lines)
