from constraint_checker import check_adjacency_conflict, check_special_requirements


def get_preferred_seats(student, hall):
    """
    Returns seats ordered by preference based on student's special requirements.
    Special requirement students get filtered seats first, others get all seats.
    """
    all_seats = hall.get_all_seats()

    if "front_row" in student.special_requirements:
        preferred = hall.get_front_row_seats()
        rest = [s for s in all_seats if s not in preferred]
        return preferred + rest

    if "back_row" in student.special_requirements:
        preferred = hall.get_back_row_seats()
        rest = [s for s in all_seats if s not in preferred]
        return preferred + rest

    if "wheelchair" in student.special_requirements:
        preferred = hall.get_aisle_seats()
        rest = [s for s in all_seats if s not in preferred]
        return preferred + rest

    return all_seats


def is_valid_placement(student, row, col, hall, students_dict):
    """
    Returns (True, "") if placement is valid, else (False, reason).
    Checks both adjacency conflicts and special requirements.
    """
    if not hall.is_seat_empty(row, col):
        return False, "Seat already occupied."

    valid, reason = check_special_requirements(student, row, col, hall)
    if not valid:
        return False, reason

    valid, reason = check_adjacency_conflict(student, row, col, hall, students_dict)
    if not valid:
        return False, reason

    return True, ""


def assign_seats(students, hall, students_dict):
    """
    Backtracking algorithm to assign seats to all students.
    Special requirement students are seated first (they have stricter constraints).
    Returns (success, failure_reasons).
    """
    # Sort: special requirement students first
    def priority(s):
        return (0 if s.special_requirements else 1, s.student_id)

    sorted_students = sorted(students, key=priority)

    failure_log = []

    def backtrack(index):
        if index == len(sorted_students):
            return True  # All students seated successfully

        student = sorted_students[index]
        preferred_seats = get_preferred_seats(student, hall)

        for (row, col) in preferred_seats:
            valid, reason = is_valid_placement(student, row, col, hall, students_dict)
            if valid:
                hall.place_student(student.student_id, row, col)
                if backtrack(index + 1):
                    return True
                hall.remove_student(row, col)  # Backtrack

        # Could not place this student — log why
        failure_log.append(build_failure_reason(student, hall, students_dict))
        return False

    success = backtrack(0)
    return success, failure_log


def build_failure_reason(student, hall, students_dict):
    """
    Explains in detail why a student could not be placed.
    """
    lines = [f"\n  Could not place: {student.name} (ID: {student.student_id})"]

    if student.special_requirements:
        lines.append(f"  Special requirements: {', '.join(student.special_requirements)}")

    if student.conflicts:
        conflict_names = []
        for cid in student.conflicts:
            if cid in students_dict:
                conflict_names.append(students_dict[cid].name)
        if conflict_names:
            lines.append(f"  Has conflicts with: {', '.join(conflict_names)}")

    # Count available empty seats
    empty_seats = [(r, c) for r in range(hall.rows)
                   for c in range(hall.cols) if hall.is_seat_empty(r, c)]
    lines.append(f"  Remaining empty seats: {len(empty_seats)}")

    if len(empty_seats) == 0:
        lines.append("  REASON: No seats left in the hall.")
    else:
        reasons = []
        if "front_row" in student.special_requirements:
            front_empty = [(r, c) for (r, c) in empty_seats if r == 0]
            if not front_empty:
                reasons.append("All front row seats are occupied.")
        if "back_row" in student.special_requirements:
            back_empty = [(r, c) for (r, c) in empty_seats if r == hall.rows - 1]
            if not back_empty:
                reasons.append("All back row seats are occupied.")
        if "wheelchair" in student.special_requirements:
            aisle = hall.get_aisle_seats()
            aisle_empty = [s for s in aisle if hall.is_seat_empty(s[0], s[1])]
            if not aisle_empty:
                reasons.append("All aisle seats are occupied.")
        if student.conflicts:
            reasons.append("Remaining seats all have conflicting neighbors already placed.")
        if not reasons:
            reasons.append("All remaining seats violate one or more constraints.")

        lines.append("  REASON: " + " | ".join(reasons))

    return "\n".join(lines)
