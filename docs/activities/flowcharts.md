# Decision Workflows and Flowcharts

## Overall workflow

Start -> Enter choice -> Validate menu choice -> Read input -> Validate data -> Calculate/report/save -> Repeat or exit.

## Risk decision tree

Start -> Calculate current percentage -> Is current < required?

- Yes: BELOW TARGET
- No: Is current < required + 5?
  - Yes: WATCH
  - No: SAFE

## Future plan decision tree

Start -> Is planned bunks > upcoming classes?

- Yes: INVALID PLAN
- No: Calculate projected attendance
  - Is projected < required? -> PLAN NOT SAFE
  - Else -> PLAN ACCEPTABLE

## Recovery decision tree

Start -> Is current attendance >= required?

- Yes: 0 recovery classes
- No: Calculate the minimum consecutive target-reaching classes
- The formula is valid for targets below 100%; the project rejects 100% because it cannot be modeled from missed past classes by the standard formula. A target of 99% is the configured upper bound.
