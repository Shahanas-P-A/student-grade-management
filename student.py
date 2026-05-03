"""
Student class for the Grade Management System.
Handles student data and related operations.
"""


class Student:
    def __init__(self, student_id: int, name: str, email: str, phone: str = "", course: str = ""):
        self.student_id = student_id
        self.name = name
        self.email = email
        self.phone = phone
        self.course = course

    def __repr__(self):
        return (
            f"Student(id={self.student_id}, name='{self.name}', "
            f"email='{self.email}', course='{self.course}')"
        )

    def display(self):
        print(f"\n{'='*40}")
        print(f"  Student ID : {self.student_id}")
        print(f"  Name       : {self.name}")
        print(f"  Email      : {self.email}")
        print(f"  Phone      : {self.phone or 'N/A'}")
        print(f"  Course     : {self.course or 'N/A'}")
        print(f"{'='*40}")

    def to_dict(self):
        return {
            "student_id": self.student_id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "course": self.course,
        }
