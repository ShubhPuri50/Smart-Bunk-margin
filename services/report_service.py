from core.attendance_calculator import attendance_percent
from core.risk_analyzer import classify_risk


def generate_subject_summary(records):
    rows = []
    for record in records:
        conducted = int(record["conducted"])
        attended = int(record["attended"])
        required = float(record["required"])
        percentage = attendance_percent(attended, conducted)
        rows.append({
            **record,
            "_percentage": percentage,
            "_risk": classify_risk(percentage, required),
        })
    return rows


def calculate_statistics(records):
    rows = generate_subject_summary(records)
    if not rows:
        return {
            "subjects": 0,
            "attended": 0,
            "conducted": 0,
            "combined": 0.0,
            "average": 0.0,
            "highest": None,
            "lowest": None,
            "below": 0,
            "watch": 0,
            "safe": 0,
        }
    attended = sum(int(row["attended"]) for row in rows)
    conducted = sum(int(row["conducted"]) for row in rows)
    average = sum(row["_percentage"] for row in rows) / len(rows)
    highest = max(rows, key=lambda row: row["_percentage"])
    lowest = min(rows, key=lambda row: row["_percentage"])
    return {
        "subjects": len(rows),
        "attended": attended,
        "conducted": conducted,
        "combined": (attended / conducted * 100) if conducted else 0.0,
        "average": average,
        "highest": highest,
        "lowest": lowest,
        "below": sum(row["_risk"] == "BELOW TARGET" for row in rows),
        "watch": sum(row["_risk"] == "WATCH" for row in rows),
        "safe": sum(row["_risk"] == "SAFE" for row in rows),
    }


def generate_insights(records):
    stats = calculate_statistics(records)
    if stats["subjects"] == 0:
        return ["No attendance records are available."]
    insights = [
        f"Highest attendance: {stats['highest']['subject']} "
        f"({stats['highest']['_percentage']:.2f}%)",
        f"Lowest attendance: {stats['lowest']['subject']} "
        f"({stats['lowest']['_percentage']:.2f}%)",
        f"Subjects below target: {stats['below']}",
    ]
    if stats["below"]:
        rows = generate_subject_summary(records)
        subjects = [
            row["subject"] for row in rows
            if row["_risk"] == "BELOW TARGET"
        ]
        insights.append(
            "Prioritize attendance in: " + ", ".join(subjects) + "."
        )
    else:
        insights.append("No subject is currently below its target.")
    return insights
