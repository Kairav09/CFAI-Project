class Hall:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.total_seats = rows * cols
        # grid[r][c] = student_id or None
        self.grid = [[None for _ in range(cols)] for _ in range(rows)]

    def get_all_seats(self):
        """Returns list of all (row, col) positions."""
        return [(r, c) for r in range(self.rows) for c in range(self.cols)]

    def get_front_row_seats(self):
        return [(0, c) for c in range(self.cols)]

    def get_back_row_seats(self):
        return [(self.rows - 1, c) for c in range(self.cols)]

    def get_aisle_seats(self):
        """First and last column — easier wheelchair access."""
        seats = []
        for r in range(self.rows):
            seats.append((r, 0))
            if self.cols > 1:
                seats.append((r, self.cols - 1))
        return seats

    def get_adjacent_seats(self, row, col):
        """Returns all directly adjacent seats (left, right, front, back)."""
        adjacent = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                adjacent.append((nr, nc))
        return adjacent

    def is_seat_empty(self, row, col):
        return self.grid[row][col] is None

    def place_student(self, student_id, row, col):
        self.grid[row][col] = student_id

    def remove_student(self, row, col):
        self.grid[row][col] = None

    def get_student_at(self, row, col):
        return self.grid[row][col]

    def reset(self):
        self.grid = [[None for _ in range(self.cols)] for _ in range(self.rows)]

    def display(self, students_dict):
        """Prints the seating grid nicely."""
        col_width = 12
        print("\n" + "=" * (col_width * self.cols + self.cols + 1))
        print(" EXAMINATION HALL SEATING ARRANGEMENT ".center(col_width * self.cols + self.cols + 1, "="))
        print("=" * (col_width * self.cols + self.cols + 1))

        # Column headers
        header = "|"
        for c in range(self.cols):
            header += f" Col {c+1:<6} |"
        print(header)
        print("-" * (col_width * self.cols + self.cols + 1))

        for r in range(self.rows):
            row_str = "|"
            for c in range(self.cols):
                sid = self.grid[r][c]
                if sid is None:
                    cell = "  EMPTY  "
                else:
                    name = students_dict[sid].name
                    cell = name[:9].center(9)
                row_str += f" {cell}  |"
            print(f"Row {r+1} {row_str}")
            print("-" * (col_width * self.cols + self.cols + 1))

        print()
