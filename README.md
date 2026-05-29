# Examination Seating Arrangement System

A console-based Python application that automatically generates examination hall seating arrangements while respecting adjacency conflicts and special student requirements. The system detects over-constrained scenarios and provides detailed explanations for failures.

---

## Features

- **Hall Setup** — Define any examination hall size using a row × column grid
- **Student Management** — Add students with auto-generated unique IDs
- **Special Requirements** — Assign seat requirements per student:
  - `front_row` — Must be seated in the first row
  - `back_row` — Must be seated in the last row
  - `wheelchair` — Must be seated in an aisle seat (first or last column)
  - `extra_space` — Cannot have an immediate left or right neighbor
- **Adjacency Conflicts** — Define pairs of students who cannot sit next to each other
- **Auto Seat Assignment** — Uses a backtracking algorithm to find a valid arrangement
- **Constraint Analysis** — Pre-checks for obvious issues before attempting seat assignment
- **Failure Explanation** — If seating fails, the system clearly explains why and suggests fixes

---

## Project Structure

```
ExamSeating/
├── main.py               # Entry point — interactive menu-driven interface
├── student.py            # Student class (ID, name, requirements, conflicts)
├── hall.py               # Hall grid — seat management and display
├── seating_engine.py     # Backtracking algorithm for seat assignment
├── constraint_checker.py # Constraint validation and over-constrained detection
└── README.md
```

---

## How to Run

### Requirements
- Python 3.x  
- No external libraries required

### Steps

1. Clone or download this repository
2. Navigate to the project folder
3. Run the program:

```bash
python main.py
```

---

## How to Use

When you run the program, you will see a menu with the following options:

```
1. Set up Examination Hall
2. Add Student
3. Add Special Requirement to Student
4. Add Adjacency Conflict Between Students
5. View All Students & Constraints
6. Generate Seating Arrangement
7. Display Current Seating Chart
8. Reset Seating Arrangement
9. Exit
```

### Recommended Flow

1. **Option 1** — Set up the hall (e.g. 3 rows, 4 columns)
2. **Option 2** — Add all students (repeat for each student)
3. **Option 3** — Add special requirements if any student needs them
4. **Option 4** — Add conflict rules between students who cannot sit adjacent
5. **Option 6** — Generate the seating arrangement
6. **Option 7** — View the final seating chart

---

## Example

**Setup:** 3 rows × 4 columns hall, 5 students

| Student | Special Requirement | Conflict With |
|---------|-------------------|---------------|
| Alice   | wheelchair        | Bob           |
| Bob     | front_row         | Alice         |
| Charlie | —                 | —             |
| Diana   | —                 | —             |
| Eve     | —                 | —             |

**Generated Output:**

```
=======================================================
======= EXAMINATION HALL SEATING ARRANGEMENT ==========
=======================================================
| Col 1      | Col 2      | Col 3      | Col 4      |
-------------------------------------------------------
Row 1 |   Alice    |  Charlie   |    Bob     |   Diana    |
-------------------------------------------------------
Row 2 |    Eve     |   EMPTY    |   EMPTY    |   EMPTY    |
-------------------------------------------------------
Row 3 |   EMPTY    |   EMPTY    |   EMPTY    |   EMPTY    |
-------------------------------------------------------
```

- Alice (wheelchair) is placed in Col 1 — an aisle seat ✔  
- Bob (front_row) is placed in Row 1 ✔  
- Alice and Bob are not adjacent to each other ✔  

---

## Over-Constrained Detection

If the system cannot find a valid arrangement, it will explain the reason clearly. For example:

```
✘  SEATING FAILED — Arrangement is over-constrained.

── Failure Details ──
  Could not place: John (ID: S003)
  Special requirements: front_row
  Remaining empty seats: 4
  REASON: All front row seats are occupied.

Suggestions:
  • Reduce the number of conflict rules.
  • Increase hall size (more rows/columns).
  • Review conflicting special requirements.
  • Remove contradictory constraints.
```

---

## Algorithm

The seat assignment uses a **backtracking algorithm**:

1. Students with special requirements are prioritized first (stricter constraints)
2. For each student, preferred seats are tried first (e.g. front row seats for a `front_row` student)
3. If a valid seat is found, the student is placed and the algorithm moves to the next student
4. If no valid seat exists, the algorithm backtracks and tries a different seat for the previous student
5. If all possibilities are exhausted, the arrangement is reported as over-constrained with a detailed failure reason

---

## Constraints Checked

| Constraint | Description |
|---|---|
| Seat Occupancy | A seat cannot be assigned to more than one student |
| Adjacency Conflict | Conflicting students are never placed in adjacent seats (left, right, front, back) |
| Front Row | Student is only placed in Row 1 |
| Back Row | Student is only placed in the last row |
| Wheelchair | Student is only placed in the first or last column |
| Extra Space | Student cannot have a neighbor immediately to their left or right |

---

## Modules Implemented

**CO1 — Agent Model & Python Essentials**
- Classes used to represent state — `Student` (stores ID, name, requirements, conflicts) and `Hall` (stores the seating grid)
- Knowledge representation via constraint rules, adjacency grid, and rule sets
- Core Python data structures — `dict`, `set`, `list` used throughout
- Trace logging and step-by-step reasoning in failure explanations

**CO2 — Search Algorithms**
- The backtracking algorithm is an implementation of **Depth First Search (DFS)** — it explores each possible seat assignment recursively and backtracks when a dead end is reached

**CO3 — Constraint Satisfaction Problems (CSP)**
- Problem modeled as a CSP — students are variables, available seats are the domain, and rules are the constraints
- Backtracking search for constraint satisfaction
- Constraint propagation via pre-constraint analysis (checks for obvious failures before search begins)
- **MRV heuristic** — students with special requirements (more constrained) are assigned seats first
- Explainability — when a constraint fails, the system clearly reports which constraint was violated and why

---

## Technologies Used

- **Language:** Python 3
- **Libraries:** None (standard library only)
- **Algorithm:** Backtracking (Constraint Satisfaction)

---

## Author

*Submitted as part of the CFAI Course Project*
