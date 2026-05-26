from student import Student
from hall import Hall
from seating_engine import assign_seats
from constraint_checker import detect_over_constrained


# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────

def print_header(title):
    print("\n" + "=" * 55)
    print(f"  {title}")
    print("=" * 55)


def print_menu():
    print_header("EXAMINATION SEATING ARRANGEMENT SYSTEM")
    print("  1. Set up Examination Hall")
    print("  2. Add Student")
    print("  3. Add Special Requirement to Student")
    print("  4. Add Adjacency Conflict Between Students")
    print("  5. View All Students & Constraints")
    print("  6. Generate Seating Arrangement")
    print("  7. Display Current Seating Chart")
    print("  8. Reset Seating Arrangement")
    print("  9. Exit")
    print("=" * 55)


def get_int_input(prompt, min_val=1, max_val=9999):
    while True:
        try:
            val = int(input(prompt))
            if min_val <= val <= max_val:
                return val
            else:
                print(f"  Please enter a number between {min_val} and {max_val}.")
        except ValueError:
            print("  Invalid input. Please enter a whole number.")


# ─────────────────────────────────────────────
#  FEATURE FUNCTIONS
# ─────────────────────────────────────────────

def setup_hall():
    print_header("SET UP EXAMINATION HALL")
    print("  Define the hall size (rows and columns of seats).")
    rows = get_int_input("  Enter number of rows    : ", 1, 20)
    cols = get_int_input("  Enter number of columns : ", 1, 20)
    hall = Hall(rows, cols)
    print(f"\n  Hall created: {rows} rows x {cols} cols = {hall.total_seats} seats.")
    return hall


def add_student(students, students_dict, id_counter):
    print_header("ADD STUDENT")
    name = input("  Enter student name : ").strip()
    if not name:
        print("  Name cannot be empty.")
        return id_counter

    sid = f"S{id_counter:03}"
    student = Student(sid, name)
    students.append(student)
    students_dict[sid] = student
    print(f"  Student added — ID: {sid}, Name: {name}")
    return id_counter + 1


def add_special_requirement(students_dict):
    print_header("ADD SPECIAL REQUIREMENT")
    if not students_dict:
        print("  No students added yet.")
        return

    print("  Students:")
    for sid, s in students_dict.items():
        print(f"    {sid} — {s.name}")

    sid = input("\n  Enter Student ID : ").strip().upper()
    if sid not in students_dict:
        print("  Student ID not found.")
        return

    print("\n  Requirements:")
    print("    1. front_row    (must sit in the first row)")
    print("    2. back_row     (must sit in the last row)")
    print("    3. wheelchair   (must sit in an aisle seat)")
    print("    4. extra_space  (no immediate left/right neighbor)")

    req_map = {"1": "front_row", "2": "back_row", "3": "wheelchair", "4": "extra_space"}
    choice = input("\n  Enter choice (1-4) : ").strip()

    if choice not in req_map:
        print("  Invalid choice.")
        return

    req = req_map[choice]
    added = students_dict[sid].add_requirement(req)
    if added:
        print(f"  Requirement '{req}' added to {students_dict[sid].name}.")
    else:
        print(f"  Requirement already exists or is invalid.")


def add_conflict(students_dict):
    print_header("ADD ADJACENCY CONFLICT")
    if len(students_dict) < 2:
        print("  Need at least 2 students to define a conflict.")
        return

    print("  Students:")
    for sid, s in students_dict.items():
        print(f"    {sid} — {s.name}")

    sid1 = input("\n  Enter first  Student ID : ").strip().upper()
    sid2 = input("  Enter second Student ID : ").strip().upper()

    if sid1 not in students_dict or sid2 not in students_dict:
        print("  One or both Student IDs not found.")
        return

    if sid1 == sid2:
        print("  A student cannot conflict with themselves.")
        return

    students_dict[sid1].add_conflict(sid2)
    students_dict[sid2].add_conflict(sid1)
    print(f"\n  Conflict added: {students_dict[sid1].name} <--> {students_dict[sid2].name}")
    print("  They will not be seated adjacent to each other.")


def view_students(students_dict):
    print_header("ALL STUDENTS & CONSTRAINTS")
    if not students_dict:
        print("  No students added yet.")
        return

    for sid, s in students_dict.items():
        print(f"\n  [{sid}] {s.name}")
        if s.special_requirements:
            print(f"        Special : {', '.join(s.special_requirements)}")
        else:
            print(f"        Special : None")

        if s.conflicts:
            conflict_names = [students_dict[cid].name for cid in s.conflicts if cid in students_dict]
            print(f"        Conflicts with : {', '.join(conflict_names)}")
        else:
            print(f"        Conflicts with : None")
    print()


def generate_seating(students, hall, students_dict):
    print_header("GENERATING SEATING ARRANGEMENT")

    if not students:
        print("  No students to seat.")
        return

    if hall is None:
        print("  Hall not set up yet. Please set up the hall first (Option 1).")
        return

    if len(students) > hall.total_seats:
        print(f"  Cannot proceed: {len(students)} students but only {hall.total_seats} seats.")
        return

    # Pre-check for obvious issues
    print("\n  [1/3] Running pre-constraint analysis...")
    warnings = detect_over_constrained(students, hall)

    if warnings:
        print("\n  ── Constraint Analysis Report ──")
        for w in warnings:
            print(f"  ⚠  {w}")
    else:
        print("  No obvious constraint violations detected.")

    # Reset and attempt seating
    hall.reset()
    print("\n  [2/3] Running backtracking seat assignment...")
    success, failure_log = assign_seats(students, hall, students_dict)

    print("\n  [3/3] Result:")
    if success:
        print("\n  ✔  Seating arrangement generated successfully!")
        print("  Use Option 7 to view the seating chart.")
    else:
        print("\n  ✘  SEATING FAILED — Arrangement is over-constrained.")
        print("\n  ── Failure Details ──")
        for reason in failure_log:
            print(reason)
        print("\n  Suggestions:")
        print("  • Reduce the number of conflict rules.")
        print("  • Increase hall size (more rows/columns).")
        print("  • Review conflicting special requirements.")
        print("  • Remove contradictory constraints (e.g. front_row + back_row on same student).")


def display_seating(hall, students_dict):
    print_header("SEATING CHART")
    if hall is None:
        print("  Hall not set up yet.")
        return
    # Check if anyone is seated
    seated = any(hall.grid[r][c] is not None
                 for r in range(hall.rows) for c in range(hall.cols))
    if not seated:
        print("  No seating arrangement generated yet. Use Option 6.")
        return
    hall.display(students_dict)


def reset_seating(hall):
    print_header("RESET SEATING")
    if hall is None:
        print("  Hall not set up yet.")
        return
    confirm = input("  Are you sure you want to reset the seating? (yes/no): ").strip().lower()
    if confirm == "yes":
        hall.reset()
        print("  Seating arrangement has been cleared.")
    else:
        print("  Reset cancelled.")


# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────

def main():
    students = []
    students_dict = {}
    hall = None
    id_counter = 1

    print("\n  Welcome to the Examination Seating Arrangement System!")
    print("  This system helps assign seats while respecting all constraints.\n")

    while True:
        print_menu()
        choice = input("  Enter your choice (1-9): ").strip()

        if choice == "1":
            hall = setup_hall()

        elif choice == "2":
            id_counter = add_student(students, students_dict, id_counter)

        elif choice == "3":
            add_special_requirement(students_dict)

        elif choice == "4":
            add_conflict(students_dict)

        elif choice == "5":
            view_students(students_dict)

        elif choice == "6":
            generate_seating(students, hall, students_dict)

        elif choice == "7":
            display_seating(hall, students_dict)

        elif choice == "8":
            reset_seating(hall)

        elif choice == "9":
            print("\n  Exiting. Goodbye!\n")
            break

        else:
            print("  Invalid choice. Please enter a number between 1 and 9.")


if __name__ == "__main__":
    main()
