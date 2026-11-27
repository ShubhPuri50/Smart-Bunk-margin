# Card Sorting and Algorithm Comparison

## Workflow cards

Student card -> Subject card -> Input-data card -> Validation card -> Attendance calculation -> Risk analysis -> Report -> CSV storage

## Input-process-output

Input: student, subject, attended classes, conducted classes, required percentage, and optional future classes.

Process: validate counts, calculate attendance, apply formulae, classify risk, update CSV, and aggregate records.

Output: percentages, bunk margin, recovery classes, projected attendance, summary, insights, and charts.

## Algorithm comparisons

| Task | Alternative 1 | Alternative 2 | Selected | Reason |
|---|---|---|---|---|
| Safe bunk margin | Repeated increment | Formula | Formula | Direct whole-number result, O(1) |
| Recovery classes | Repeated simulated attendance | Formula | Formula | Direct ceiling result, O(1) |
| Subject search | Linear list scan | Dictionary lookup | Dictionary | Expected O(1) lookup; current subject index in `storage/csv_manager.py` |
| Risk classification | Independent conditions | Nested decision logic | Nested logic | Matches the below-target, watch, and safe decision tree |

## Subject lookup demonstration

`create_subject_index(records)` stores subjects by lowercase names. `find_subject(subject_index, subject_name)` can be represented by `subject_index.get(subject_name.lower())`.
