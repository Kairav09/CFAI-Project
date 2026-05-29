def check_adjacency_conflict(student, row, col, hall, students_dict):
    """
    Returns (is_valid, reason).
    Checks if placing this student at (row, col) violates any conflict constraints.
    """
    adjacent_seats = hall.get_adjacent_seats(row, col)
    for (ar, ac) in adjacent_seats:
        neighbor_id = hall.get_student_at(ar, ac)
        if neighbor_id is not None:
            # Check if student conflicts with this neighbor
            if neighbor_id in student.conflicts:
                neighbor_name = students_dict[neighbor_id].name
                return False, (f"{student.name} cannot sit adjacent to {neighbor_name} "
                               f"(conflict rule)")
            # Check reverse conflict too
            neighbor = students_dict[neighbor_id]
            if student.student_id in neighbor.conflicts:
                neighbor_name = neighbor.name
                return False, (f"{neighbor_name} cannot sit adjacent to {student.name} "
                               f"(conflict rule)")
    return True, ""


def check_special_requirements(student, row, col, hall):
    """
    Returns (is_valid, reason).
    Checks if a seat satisfies the student's special requirements.
    """
    for req in student.special_requirements:
        if req == "front_row":
            if row != 0:
                return False, f"{student.name} requires a front row seat (Row 1)."
        elif req == "back_row":
            if row != hall.rows - 1:
                return False, f"{student.name} requires a back row seat (Row {hall.rows})."
        elif req == "wheelchair":
            aisle_seats = hall.get_aisle_seats()
            if (row, col) not in aisle_seats:
                return False, f"{student.name} requires an aisle seat (wheelchair access)."
        elif req == "extra_space":
            # Extra space: student cannot have neighbors on left AND right
            has_left = col > 0 and hall.get_student_at(row, col - 1) is not None
            has_right = col < hall.cols - 1 and hall.get_student_at(row, col + 1) is not None
            if has_left or has_right:
                return False, f"{student.name} requires extra space (no immediate left/right neighbor)."
    return True, ""


def detect_over_constrained(students, hall):
    """
    Analyzes constraints BEFORE attempting seating to catch obvious failures early.
    Returns a list of warning/failure messages.
    """
    issues = []
    total_seats = hall.total_seats
    total_students = len(students)

    # Basic capacity check
    if total_students > total_seats:
        issues.append(f"CAPACITY EXCEEDED: {total_students} students but only "
                      f"{total_seats} seats available ({hall.rows} rows x {hall.cols} cols).")

    # Front row demand check
    front_row_needed = [s for s in students if "front_row" in s.special_requirements]
    if len(front_row_needed) > hall.cols:
        names = ", ".join([s.name for s in front_row_needed])
        issues.append(f"FRONT ROW OVERFLOW: {len(front_row_needed)} students need front row "
                      f"but only {hall.cols} seats available there. "
                      f"Affected: {names}.")

    # Back row demand check
    back_row_needed = [s for s in students if "back_row" in s.special_requirements]
    if len(back_row_needed) > hall.cols:
        names = ", ".join([s.name for s in back_row_needed])
        issues.append(f"BACK ROW OVERFLOW: {len(back_row_needed)} students need back row "
                      f"but only {hall.cols} seats available there. "
                      f"Affected: {names}.")

    # Wheelchair / aisle seat check
    wheelchair_needed = [s for s in students if "wheelchair" in s.special_requirements]
    aisle_seats = hall.get_aisle_seats()
    if len(wheelchair_needed) > len(aisle_seats):
        names = ", ".join([s.name for s in wheelchair_needed])
        issues.append(f"AISLE SEAT SHORTAGE: {len(wheelchair_needed)} students need aisle seats "
                      f"but only {len(aisle_seats)} aisle seats exist. "
                      f"Affected: {names}.")

    # Mutual conflict check — if A conflicts with B and B conflicts with A, flag it
    student_map = {s.student_id: s for s in students}
    flagged_pairs = set()
    for s in students:
        for conflict_id in s.conflicts:
            pair = tuple(sorted([s.student_id, conflict_id]))
            if pair not in flagged_pairs:
                flagged_pairs.add(pair)
                if conflict_id in student_map:
                    other = student_map[conflict_id]
                    issues.append(f"CONFLICT NOTED: {s.name} <--> {other.name} "
                                  f"cannot be seated adjacent to each other.")

    return issues
