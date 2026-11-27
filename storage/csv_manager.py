import csv
import os
from config import DATA_FILE, FIELDNAMES
from core.validators import validate_attendance


def load_records(filename=DATA_FILE):
    if not os.path.exists(filename) or os.path.getsize(filename) == 0:
        return []
    with open(filename, "r", newline="", encoding="utf-8") as file:
        records = []
        for row in csv.DictReader(file):
            records.append({
                "subject": str(row["subject"]).strip(),
                "conducted": int(row["conducted"]),
                "attended": int(row["attended"]),
                "required": float(row["required"]),
            })
        return records


def save_record(subject, conducted, attended, required, filename=DATA_FILE):
    subject = str(subject).strip()
    if not subject:
        raise ValueError("subject name cannot be empty")
    validate_attendance(attended, conducted, required)
    file_exists = os.path.exists(filename) and os.path.getsize(filename) > 0
    with open(filename, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        if not file_exists:
            writer.writeheader()
        writer.writerow({
            "subject": subject,
            "conducted": conducted,
            "attended": attended,
            "required": float(required),
        })


def upsert_record(subject, conducted, attended, required, filename=DATA_FILE):
    subject = str(subject).strip()
    if not subject:
        raise ValueError("subject name cannot be empty")
    validate_attendance(attended, conducted, required)
    records = load_records(filename)
    index = create_subject_index(records)
    key = subject.lower()
    record = {
        "subject": subject,
        "conducted": conducted,
        "attended": attended,
        "required": float(required),
    }
    if key in index:
        for i, existing in enumerate(records):
            if existing["subject"].lower() == key:
                records[i] = record
                break
    else:
        records.append(record)
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(records)


def create_subject_index(records):
    return {
        str(record["subject"]).lower(): record
        for record in records
    }
