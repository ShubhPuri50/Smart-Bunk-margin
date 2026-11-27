from .attendance_calculator import attendance_percent


def projected_attendance(attended, conducted, upcoming, planned_bunks):
    if not isinstance(upcoming, int) or isinstance(upcoming, bool) or upcoming < 0:
        raise ValueError("upcoming classes must be a non-negative whole number")
    if (not isinstance(planned_bunks, int) or isinstance(planned_bunks, bool)
            or planned_bunks < 0 or planned_bunks > upcoming):
        raise ValueError("planned bunks must be between 0 and upcoming classes")
    if conducted < 1 or attended < 0 or attended > conducted:
        raise ValueError("existing attendance counts are invalid")
    final_attended = attended + (upcoming - planned_bunks)
    final_conducted = conducted + upcoming
    return attendance_percent(final_attended, final_conducted)


def check_future_plan(attended, conducted, upcoming, planned_bunks, required):
    if planned_bunks > upcoming:
        return "INVALID PLAN"
    projection = projected_attendance(attended, conducted, upcoming, planned_bunks)
    return "PLAN ACCEPTABLE" if projection >= required else "PLAN NOT SAFE"
