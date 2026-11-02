"""
Flask Student Records Application with SQLite
Subject: Web Application Frameworks (WAF) Lab
Author: Jeyavardhan Lekkala (Roll No: 2024009057)
"""

import os
import sqlite3
from flask import Flask, render_template

app = Flask(__name__)

# SQLite database file path in the application directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "students.db")


def get_db_connection():
    """Create a connection to SQLite database with Row factory."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize database table and insert default sample records if empty."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create students table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            year TEXT NOT NULL
        )
    """)

    # Populate sample records if table is currently empty
    cursor.execute("SELECT COUNT(*) FROM students")
    count = cursor.fetchone()[0]

    if count == 0:
        sample_students = [
            ("Jeyavardhan Lekkala", "Computer Science & Engineering", "3rd Year"),
            ("Sarah Jenkins", "Information Technology", "3rd Year"),
            ("Rahul Sharma", "Computer Science & Engineering", "2nd Year"),
            ("Priya Patel", "Electronics & Communication", "4th Year"),
            ("Alex Rivera", "Mechanical Engineering", "1st Year"),
        ]
        cursor.executemany(
            "INSERT INTO students (name, department, year) VALUES (?, ?, ?)",
            sample_students,
        )
        conn.commit()

    conn.close()


# Initialize database upon module import so table and records are guaranteed ready
init_db()


@app.route("/")
def index():
    """Retrieve all student records from SQLite and render template."""
    conn = get_db_connection()
    students = conn.execute(
        "SELECT id, name, department, year FROM students ORDER BY id ASC"
    ).fetchall()
    conn.close()
    return render_template("index.html", students=students)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
