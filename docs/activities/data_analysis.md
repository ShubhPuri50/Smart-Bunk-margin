# Data Interpretation and Reporting

The reporting module reads the actual CSV records and calculates both:

- Subject-wise average attendance: the mean of each subject percentage.
- Combined attendance: total attended classes divided by total conducted classes.

For every subject, the report shows attended and conducted counts, percentage, and risk label.

`calculate_statistics()` calculates subject count, totals, average, combined percentage, highest subject, lowest subject, and SAFE/WATCH/BELOW TARGET counts.

`generate_insights()` derives priorities and recommendations from the loaded records. `generate_charts()` creates:

1. Subject-wise attendance against required thresholds.
2. SAFE/WATCH/BELOW TARGET distribution.
3. Current attendance compared with the projection bar.

Charts are written to the `charts/` directory as PNG files and use Matplotlib with the non-interactive `Agg` backend.
