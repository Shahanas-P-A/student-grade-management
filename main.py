"""
Student Grade Management System — Main CLI
==========================================
A command-line application to manage student records and grades
using MySQL as the backend database.

Usage:
    python main.py

Requirements:
    pip install mysql-connector-python
"""

import os
from database import Database
from student import Student
from grade import Grade

# ─────────────────────────────────────────────
#  DB Configuration  (edit or use env vars)
# ─────────────────────────────────────────────
DB_CONFIG = {
    "host":     os.getenv("DB_HOST",     "localhost"),
    "user":     os.getenv("DB_USER",     "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME",     "grade_management"),
}


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def pause():
    input("\nPress Enter to continue...")


# ─────────────────────────────────────────────
#  Student menus
# ─────────────────────────────────────────────

def menu_add_student(db: Database):
    print("\n── Add New Student ──")
    name   = input("Full name   : ").strip()
    email  = input("Email       : ").strip()
    phone  = input("Phone       : ").strip()
    course = input("Course      : ").strip()
    if not name or not email:
        print("❌ Name and email are required.")
        return
    student = db.add_student(name, email, phone, course)
    if student:
        print(f"✅ Student added successfully!")
        student.display()


def menu_view_students(db: Database):
    print("\n── All Students ──")
    students = db.get_all_students()
    if not students:
        print("No students found.")
        return
    print(f"\n{'ID':<6} {'Name':<25} {'Email':<30} {'Course':<20}")
    print("-" * 85)
    for s in students:
        print(f"{s.student_id:<6} {s.name:<25} {s.email:<30} {s.course or 'N/A':<20}")


def menu_update_student(db: Database):
    print("\n── Update Student ──")
    try:
        sid = int(input("Student ID to update: "))
    except ValueError:
        print("❌ Invalid ID.")
        return
    student = db.get_student_by_id(sid)
    if not student:
        print("❌ Student not found.")
        return
    student.display()
    print("Leave blank to keep current value.")
    name   = input(f"New name   [{student.name}]   : ").strip() or None
    email  = input(f"New email  [{student.email}]  : ").strip() or None
    phone  = input(f"New phone  [{student.phone}]  : ").strip()
    course = input(f"New course [{student.course}] : ").strip()
    success = db.update_student(sid, name=name, email=email,
                                phone=phone or None, course=course or None)
    print("✅ Student updated." if success else "❌ Update failed.")


def menu_delete_student(db: Database):
    print("\n── Delete Student ──")
    try:
        sid = int(input("Student ID to delete: "))
    except ValueError:
        print("❌ Invalid ID.")
        return
    student = db.get_student_by_id(sid)
    if not student:
        print("❌ Student not found.")
        return
    student.display()
    confirm = input("Are you sure? (yes/no): ").strip().lower()
    if confirm == "yes":
        success = db.delete_student(sid)
        print("✅ Student deleted." if success else "❌ Deletion failed.")
    else:
        print("Cancelled.")


# ─────────────────────────────────────────────
#  Grade menus
# ─────────────────────────────────────────────

def menu_add_grade(db: Database):
    print("\n── Add Grade ──")
    try:
        sid = int(input("Student ID : "))
    except ValueError:
        print("❌ Invalid ID.")
        return
    if not db.get_student_by_id(sid):
        print("❌ Student not found.")
        return
    subject = input("Subject    : ").strip()
    try:
        marks     = float(input("Marks      : "))
        max_marks = float(input("Max marks  [100]: ") or 100)
    except ValueError:
        print("❌ Invalid marks.")
        return
    grade = db.add_grade(sid, subject, marks, max_marks)
    if grade:
        print("✅ Grade added!")
        grade.display()


def menu_view_grades(db: Database):
    print("\n── View Student Grades ──")
    try:
        sid = int(input("Student ID: "))
    except ValueError:
        print("❌ Invalid ID.")
        return
    student = db.get_student_by_id(sid)
    if not student:
        print("❌ Student not found.")
        return
    grades = db.get_grades_by_student(sid)
    avg    = db.get_student_average(sid)
    print(f"\nGrades for: {student.name}")
    if not grades:
        print("No grades recorded.")
        return
    print(f"\n{'GID':<6} {'Subject':<25} {'Marks':<10} {'Max':<8} {'%':<8} {'Grade'}")
    print("-" * 65)
    for g in grades:
        print(f"{g.grade_id:<6} {g.subject:<25} {g.marks:<10} {g.max_marks:<8} {g.percentage:<8.2f} {g.letter_grade}")
    print(f"\n  Overall Average: {avg}%" if avg is not None else "\n  No average available.")


def menu_update_grade(db: Database):
    print("\n── Update Grade ──")
    try:
        gid   = int(input("Grade ID   : "))
        marks = float(input("New marks  : "))
        raw   = input("New max marks (leave blank to keep): ").strip()
        max_m = float(raw) if raw else None
    except ValueError:
        print("❌ Invalid input.")
        return
    success = db.update_grade(gid, marks, max_m)
    print("✅ Grade updated." if success else "❌ Grade not found or update failed.")


def menu_delete_grade(db: Database):
    print("\n── Delete Grade ──")
    try:
        gid = int(input("Grade ID to delete: "))
    except ValueError:
        print("❌ Invalid ID.")
        return
    confirm = input("Are you sure? (yes/no): ").strip().lower()
    if confirm == "yes":
        success = db.delete_grade(gid)
        print("✅ Grade deleted." if success else "❌ Grade not found.")
    else:
        print("Cancelled.")


# ─────────────────────────────────────────────
#  Main menu
# ─────────────────────────────────────────────

STUDENT_MENU = {
    "1": ("Add Student",    menu_add_student),
    "2": ("View Students",  menu_view_students),
    "3": ("Update Student", menu_update_student),
    "4": ("Delete Student", menu_delete_student),
    "5": ("Back",           None),
}

GRADE_MENU = {
    "1": ("Add Grade",    menu_add_grade),
    "2": ("View Grades",  menu_view_grades),
    "3": ("Update Grade", menu_update_grade),
    "4": ("Delete Grade", menu_delete_grade),
    "5": ("Back",         None),
}


def run_sub_menu(db: Database, menu: dict, title: str):
    while True:
        print(f"\n{'='*40}")
        print(f"  {title}")
        print(f"{'='*40}")
        for key, (label, _) in menu.items():
            print(f"  [{key}] {label}")
        choice = input("\nEnter choice: ").strip()
        if choice not in menu:
            print("❌ Invalid option.")
            continue
        label, func = menu[choice]
        if func is None:
            break
        func(db)
        pause()


def main():
    print("\n" + "="*50)
    print("  Student Grade Management System")
    print("="*50)
    db = Database(**DB_CONFIG)
    if not db.connection:
        print("❌ Could not connect to the database. Check your DB_CONFIG.")
        return

    while True:
        print(f"\n{'='*40}")
        print("  MAIN MENU")
        print(f"{'='*40}")
        print("  [1] Manage Students")
        print("  [2] Manage Grades")
        print("  [0] Exit")
        choice = input("\nEnter choice: ").strip()

        if choice == "1":
            run_sub_menu(db, STUDENT_MENU, "STUDENT MANAGEMENT")
        elif choice == "2":
            run_sub_menu(db, GRADE_MENU, "GRADE MANAGEMENT")
        elif choice == "0":
            db.close()
            print("\n👋 Goodbye!")
            break
        else:
            print("❌ Invalid option.")


if __name__ == "__main__":
    main()
