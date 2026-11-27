import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from services.report_service import generate_subject_summary, calculate_statistics


def generate_charts(records, output_dir="docs/assets/charts"):
    os.makedirs(output_dir, exist_ok=True)
    rows = generate_subject_summary(records)
    if not rows:
        return []

    names = [row["subject"] for row in rows]
    percentages = [row["_percentage"] for row in rows]
    thresholds = [float(row["required"]) for row in rows]

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(names, percentages, color="#4C78A8")
    ax.plot(names, thresholds, "r--", label="Required")
    ax.set_ylabel("Attendance (%)")
    ax.set_ylim(0, 100)
    ax.tick_params(axis="x", rotation=30)
    ax.legend()
    fig.tight_layout()
    chart1 = os.path.join(output_dir, "subject_attendance.png")
    fig.savefig(chart1)
    plt.close(fig)

    stats = calculate_statistics(rows)
    labels = ["SAFE", "WATCH", "BELOW TARGET"]
    counts = [stats["safe"], stats["watch"], stats["below"]]
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.pie(counts, labels=labels, autopct="%1.0f%%",
           colors=["#59A14F", "#F2CF5B", "#E15759"])
    ax.set_title("Attendance Status Distribution")
    fig.tight_layout()
    chart2 = os.path.join(output_dir, "status_distribution.png")
    fig.savefig(chart2)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 5))
    x = range(len(rows))
    ax.bar([i - 0.18 for i in x], percentages, width=0.36,
           label="Current", color="#4C78A8")
    ax.bar([i + 0.18 for i in x], percentages, width=0.36,
           label="No-absence baseline", color="#72B7B2")
    ax.set_xticks(list(x), names)
    ax.set_ylabel("Attendance (%)")
    ax.set_ylim(0, 100)
    ax.legend()
    fig.tight_layout()
    chart3 = os.path.join(output_dir, "attendance_projection.png")
    fig.savefig(chart3)
    plt.close(fig)
    return [chart1, chart2, chart3]
