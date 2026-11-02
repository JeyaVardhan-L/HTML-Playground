# Flask Student Records Application with SQLite

**Subject:** Web Application Frameworks (WAF) Lab — Final Practical Assignment  
**Student Name:** Jeyavardhan Lekkala  
**Roll Number:** 2024009057  
**Technology Stack:** Python 3, Flask, SQLite3, Jinja2 Templates  

---

## 1. Overview

This is a lightweight, beginner-friendly web application built with **Flask** and **SQLite3**. It demonstrates:
- Connecting to an SQLite database (`students.db`).
- Creating a `students` table schema with columns: `id`, `name`, `department`, and `year`.
- Automatically initializing the database with sample student records on startup if the database is empty.
- Dynamically querying records using Python's native `sqlite3` cursor.
- Rendering retrieved data inside a clean, responsive HTML table using Jinja2 templating.

---

## 2. Directory Structure

```text
flask-app/
├── app.py                # Main Flask application with SQLite connection & route logic
├── requirements.txt      # Python dependencies (Flask)
├── README.md             # Setup and execution guide
└── templates/
    └── index.html        # HTML template rendering the student records table
```

---

## 3. Installation & Execution

### Step 1: Navigate to the directory
```bash
cd Assignment-8/flask-app
```

### Step 2: Install dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run the application
```bash
python app.py
```

### Step 4: Open in your browser
Open your browser and navigate to:
```text
http://127.0.0.1:5000/
```

---

## 4. How Database Initialization & Data Retrieval Work

1. **Connection:** When `get_db_connection()` is called, it opens a connection to `students.db` in the same folder and sets `conn.row_factory = sqlite3.Row` so column names can be accessed as dictionary keys in templates.
2. **Auto-Initialization:** In `init_db()`, the application executes `CREATE TABLE IF NOT EXISTS students (...)`. It checks if `SELECT COUNT(*)` is zero; if so, it inserts 5 sample student records using parameterized `cursor.executemany()` to prevent SQL injection.
3. **Data Retrieval:** On handling `GET /`, the route executes:
   ```python
   students = conn.execute("SELECT id, name, department, year FROM students ORDER BY id ASC").fetchall()
   ```
   and passes `students` to `render_template("index.html", students=students)`.
