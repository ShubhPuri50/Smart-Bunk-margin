# Smart Bunk Margin & Attendance Defense Planner

**Institution:** Bennett University, School of Computer Science Engineering and Technology  
**Course:** Computational Thinking and Programming (2026CSAE100)  
**Academic year:** 2026-27  
**Student:** Shubh Puri  
**Enrollment:** S26CSEU3581

A modular Python application for subject-wise attendance planning. It calculates attendance percentages, safe bunk margins, recovery classes, future projections, risk labels, summaries, insights, and charts.

## Run

```bash
python main.py
```

The compatibility entry point is also available:

```bash
python smart_bunk_margin_planner.py
```

## Test

Install optional visualization dependencies:

```bash
pip install -r requirements.txt
```

Run the regression suite:

```bash
python -m unittest discover -s tests -v
```

## Project Structure

- `main.py` - finalized 13-option command-line application
- `smart_bunk_margin_planner.py` - backward-compatible entry point
- `config.py` - shared configuration
- `core/` - validation, calculations, projections, and risk logic
- `models/` - Student, SubjectAttendance, planner, and report classes
- `storage/` - CSV persistence and subject indexing
- `services/` - analysis and reporting services
- `visualization/` - Matplotlib chart generation
- `data/` - attendance CSV data
- `tests/` - automated regression tests
- `docs/`
  - `activities/` - activity and technical evidence
  - `assets/` - report, presentation, flowchart, and charts
  - `results/` - test logs and sample output

See [docs/index.md](docs/index.md) for project documentation.

## Data and Privacy

`data/attendance_data.csv` contains illustrative sample records only. The application does not connect to university systems.
