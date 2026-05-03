# Student Grade Management System

A command-line application built with **Python** and **MySQL** to manage student records and grades. Follows OOP design with dedicated classes for `Student`, `Grade`, and `Database`.

## Features

- ➕ Add, view, update, delete student records
- 📊 Add, view, update, delete grades per student
- 🔤 Automatic letter grade calculation (A+, A, B, C, D, F)
- 📈 Per-student average percentage
- 🔗 Referential integrity via MySQL foreign keys

## Project Structure

```
student-grade-management/
├── main.py          # CLI entry point
├── student.py       # Student class
├── grade.py         # Grade class (with letter grade logic)
├── database.py      # Database class (MySQL CRUD)
├── requirements.txt
└── database/
    └── schema.sql   # DB setup + sample data
```

## Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Create the database
```bash
mysql -u root -p < database/schema.sql
```

### 3. Configure connection
Edit `DB_CONFIG` in `main.py` or set environment variables:
```bash
export DB_HOST=localhost
export DB_USER=root
export DB_PASSWORD=yourpassword
export DB_NAME=grade_management
```

### 4. Run the app
```bash
python main.py
```

## Grade Scale

| Percentage | Letter |
|------------|--------|
| 90 – 100   | A+     |
| 80 – 89    | A      |
| 70 – 79    | B      |
| 60 – 69    | C      |
| 50 – 59    | D      |
| Below 50   | F      |

## Technologies

- **Python 3.8+**
- **MySQL 8.0+**
- **mysql-connector-python**
