class Student:
    def __init__(self, student_id, name):
        self.student_id = student_id
        self.name = name
        self.special_requirements = []
        self.conflicts = set()

    def add_requirement(self, requirement):
        valid = ["wheelchair", "front_row", "extra_space", "back_row"]
        if requirement in valid:
            if requirement not in self.special_requirements:
                self.special_requirements.append(requirement)
                return True
        return False

    def add_conflict(self, other_id):
        self.conflicts.add(other_id)

    def __str__(self):
        return f"{self.student_id}:{self.name}"
