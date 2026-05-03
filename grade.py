"""
Grade class for the Grade Management System.
Handles grade/marks data and letter grade computation.
"""


class Grade:
    GRADE_THRESHOLDS = [
        (90, "A+"),
        (80, "A"),
        (70, "B"),
        (60, "C"),
        (50, "D"),
        (0,  "F"),
    ]

    def __init__(self, grade_id: int, student_id: int, subject: str, marks: float, max_marks: float = 100):
        self.grade_id = grade_id
        self.student_id = student_id
        self.subject = subject
        self.marks = marks
        self.max_marks = max_marks

    @property
    def percentage(self) -> float:
        return (self.marks / self.max_marks) * 100 if self.max_marks > 0 else 0

    @property
    def letter_grade(self) -> str:
        pct = self.percentage
        for threshold, letter in self.GRADE_THRESHOLDS:
            if pct >= threshold:
                return letter
        return "F"

    def __repr__(self):
        return (
            f"Grade(id={self.grade_id}, student_id={self.student_id}, "
            f"subject='{self.subject}', marks={self.marks}/{self.max_marks}, "
            f"grade='{self.letter_grade}')"
        )

    def display(self):
        print(f"\n{'='*40}")
        print(f"  Grade ID   : {self.grade_id}")
        print(f"  Student ID : {self.student_id}")
        print(f"  Subject    : {self.subject}")
        print(f"  Marks      : {self.marks} / {self.max_marks}")
        print(f"  Percentage : {self.percentage:.2f}%")
        print(f"  Letter     : {self.letter_grade}")
        print(f"{'='*40}")

    def to_dict(self):
        return {
            "grade_id": self.grade_id,
            "student_id": self.student_id,
            "subject": self.subject,
            "marks": self.marks,
            "max_marks": self.max_marks,
            "percentage": round(self.percentage, 2),
            "letter_grade": self.letter_grade,
        }
