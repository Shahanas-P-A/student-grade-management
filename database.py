"""
Database class for the Grade Management System.
Handles all MySQL operations using mysql-connector-python.
"""

import mysql.connector
from mysql.connector import Error
from student import Student
from grade import Grade
from typing import List, Optional


class Database:
    def __init__(self, host: str, user: str, password: str, database: str):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.connect()
        self.create_tables()

    # ──────────────────────────────────────────
    #  Connection
    # ──────────────────────────────────────────

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
            )
            if self.connection.is_connected():
                print("✅ Connected to MySQL database.")
        except Error as e:
            print(f"❌ Error connecting to MySQL: {e}")
            self.connection = None

    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("🔌 Database connection closed.")

    def _cursor(self):
        if not self.connection or not self.connection.is_connected():
            self.connect()
        return self.connection.cursor(dictionary=True)

    # ──────────────────────────────────────────
    #  Schema
    # ──────────────────────────────────────────

    def create_tables(self):
        cursor = self._cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                student_id   INT AUTO_INCREMENT PRIMARY KEY,
                name         VARCHAR(100) NOT NULL,
                email        VARCHAR(150) UNIQUE NOT NULL,
                phone        VARCHAR(20),
                course       VARCHAR(100)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS grades (
                grade_id    INT AUTO_INCREMENT PRIMARY KEY,
                student_id  INT NOT NULL,
                subject     VARCHAR(100) NOT NULL,
                marks       FLOAT NOT NULL,
                max_marks   FLOAT NOT NULL DEFAULT 100,
                FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
            )
        """)
        self.connection.commit()
        cursor.close()

    # ──────────────────────────────────────────
    #  Student CRUD
    # ──────────────────────────────────────────

    def add_student(self, name: str, email: str, phone: str = "", course: str = "") -> Optional[Student]:
        try:
            cursor = self._cursor()
            cursor.execute(
                "INSERT INTO students (name, email, phone, course) VALUES (%s, %s, %s, %s)",
                (name, email, phone, course),
            )
            self.connection.commit()
            student_id = cursor.lastrowid
            cursor.close()
            return Student(student_id, name, email, phone, course)
        except Error as e:
            print(f"❌ Error adding student: {e}")
            return None

    def get_all_students(self) -> List[Student]:
        cursor = self._cursor()
        cursor.execute("SELECT * FROM students ORDER BY student_id")
        rows = cursor.fetchall()
        cursor.close()
        return [Student(**row) for row in rows]

    def get_student_by_id(self, student_id: int) -> Optional[Student]:
        cursor = self._cursor()
        cursor.execute("SELECT * FROM students WHERE student_id = %s", (student_id,))
        row = cursor.fetchone()
        cursor.close()
        return Student(**row) if row else None

    def update_student(self, student_id: int, name: str = None, email: str = None,
                       phone: str = None, course: str = None) -> bool:
        student = self.get_student_by_id(student_id)
        if not student:
            return False
        name   = name   or student.name
        email  = email  or student.email
        phone  = phone  if phone  is not None else student.phone
        course = course if course is not None else student.course
        try:
            cursor = self._cursor()
            cursor.execute(
                "UPDATE students SET name=%s, email=%s, phone=%s, course=%s WHERE student_id=%s",
                (name, email, phone, course, student_id),
            )
            self.connection.commit()
            cursor.close()
            return True
        except Error as e:
            print(f"❌ Error updating student: {e}")
            return False

    def delete_student(self, student_id: int) -> bool:
        try:
            cursor = self._cursor()
            cursor.execute("DELETE FROM students WHERE student_id = %s", (student_id,))
            self.connection.commit()
            affected = cursor.rowcount
            cursor.close()
            return affected > 0
        except Error as e:
            print(f"❌ Error deleting student: {e}")
            return False

    # ──────────────────────────────────────────
    #  Grade CRUD
    # ──────────────────────────────────────────

    def add_grade(self, student_id: int, subject: str, marks: float, max_marks: float = 100) -> Optional[Grade]:
        try:
            cursor = self._cursor()
            cursor.execute(
                "INSERT INTO grades (student_id, subject, marks, max_marks) VALUES (%s, %s, %s, %s)",
                (student_id, subject, marks, max_marks),
            )
            self.connection.commit()
            grade_id = cursor.lastrowid
            cursor.close()
            return Grade(grade_id, student_id, subject, marks, max_marks)
        except Error as e:
            print(f"❌ Error adding grade: {e}")
            return None

    def get_grades_by_student(self, student_id: int) -> List[Grade]:
        cursor = self._cursor()
        cursor.execute("SELECT * FROM grades WHERE student_id = %s ORDER BY subject", (student_id,))
        rows = cursor.fetchall()
        cursor.close()
        return [Grade(**row) for row in rows]

    def update_grade(self, grade_id: int, marks: float, max_marks: float = None) -> bool:
        try:
            cursor = self._cursor()
            if max_marks is not None:
                cursor.execute(
                    "UPDATE grades SET marks=%s, max_marks=%s WHERE grade_id=%s",
                    (marks, max_marks, grade_id),
                )
            else:
                cursor.execute("UPDATE grades SET marks=%s WHERE grade_id=%s", (marks, grade_id))
            self.connection.commit()
            affected = cursor.rowcount
            cursor.close()
            return affected > 0
        except Error as e:
            print(f"❌ Error updating grade: {e}")
            return False

    def delete_grade(self, grade_id: int) -> bool:
        try:
            cursor = self._cursor()
            cursor.execute("DELETE FROM grades WHERE grade_id = %s", (grade_id,))
            self.connection.commit()
            affected = cursor.rowcount
            cursor.close()
            return affected > 0
        except Error as e:
            print(f"❌ Error deleting grade: {e}")
            return False

    def get_student_average(self, student_id: int) -> Optional[float]:
        cursor = self._cursor()
        cursor.execute(
            "SELECT AVG((marks/max_marks)*100) AS avg_pct FROM grades WHERE student_id = %s",
            (student_id,),
        )
        row = cursor.fetchone()
        cursor.close()
        return round(row["avg_pct"], 2) if row and row["avg_pct"] is not None else None
