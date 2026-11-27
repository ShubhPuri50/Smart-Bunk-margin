# Problem Decomposition

The application is divided into input, validation, calculation, risk analysis, storage, reporting, visualization, and presentation modules.

## Functional modules

| Responsibility | Module |
|---|---|
| Menu and interaction | `main.py` |
| Student and subject objects | `models/` |
| Attendance formulas | `core/attendance_calculator.py` |
| Input validation | `core/validators.py` |
| Projection and bunk plan | `core/projection.py` |
| Risk decisions | `core/risk_analyzer.py` |
| CSV persistence | `storage/csv_manager.py` |
| Business coordination | `services/attendance_service.py` |
| Summary and insights | `services/report_service.py` |
| Charts | `visualization/charts.py` |

The compatibility module `smart_bunk_margin_planner.py` exposes the original function names while delegating implementation to the modular packages.
