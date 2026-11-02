# Django Student Records Application with SQLite

**Subject:** Web Application Frameworks (WAF) Lab — Final Practical Assignment  
**Student Name:** Jeyavardhan Lekkala  
**Roll Number:** 2024009057  
**Technology Stack:** Python 3, Django, SQLite3, Django ORM, Django Templates  

---

## 1. Overview

This is a clean, minimal, beginner-friendly web application built with **Django** and **SQLite3**. It demonstrates:
- Configuring Django with an SQLite database backend (`db.sqlite3`).
- Defining a `Student` model schema with fields: `id` (auto-generated primary key), `name`, `department`, and `year`.
- Generating and applying Django schema migrations (`makemigrations` and `migrate`).
- Repeatable sample record initialization using either the custom management command (`seed_students`) or automatic on-demand check on view execution.
- Querying records using Django ORM (`Student.objects.all().order_by('id')`).
- Rendering the records dynamically inside an HTML template using Django's template engine (`{% for student in students %}`).

---

## 2. Directory Structure

```text
django-app/
├── manage.py                     # Django management script
├── requirements.txt              # Project dependencies (Django)
├── README.md                     # Setup and execution guide
├── student_portal/               # Project configuration package
│   ├── __init__.py
│   ├── settings.py               # Django configuration (SQLite, INSTALLED_APPS)
│   ├── urls.py                   # Root URL dispatcher
│   ├── wsgi.py
│   └── asgi.py
└── students/                     # Application package
    ├── __init__.py
    ├── models.py                 # Student model declaration
    ├── views.py                  # View function retrieving data via ORM
    ├── urls.py                   # App URL routing
    ├── admin.py
    ├── migrations/               # Database migration files
    │   ├── 0001_initial.py       # Initial schema migration
    │   └── __init__.py
    ├── management/
    │   └── commands/
    │       └── seed_students.py  # Repeatable sample data seeding command
    └── templates/
        └── students/
            └── student_list.html # HTML template rendering the student table
```

---

## 3. Installation & Execution

### Step 1: Navigate to the directory
```bash
cd Assignment-8/django-app
```

### Step 2: Install dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run database migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 4: Seed sample student records (Optional / Repeatable)
```bash
python manage.py seed_students
```
*(Note: If you skip this command, the application view automatically seeds the records on first visit if the table is empty.)*

### Step 5: Start the development server
```bash
python manage.py runserver 8000
```

### Step 6: Open in your browser
Open your browser and navigate to:
```text
http://127.0.0.1:8000/
```

---

## 4. How Django Migrations & ORM Retrieval Work

1. **Model Definition:** The `Student` model in `students/models.py` specifies `name`, `department`, and `year`. Django automatically supplies the integer primary key `id`.
2. **Migrations:** Running `python manage.py makemigrations` inspects `models.py` and produces `students/migrations/0001_initial.py`. Running `python manage.py migrate` translates this into an SQLite `CREATE TABLE "students_student" (...)` statement.
3. **ORM Data Retrieval:** The view in `students/views.py` queries the database through Django's Object-Relational Mapper without raw SQL:
   ```python
   students = Student.objects.all().order_by('id')
   ```
   and renders the records in `students/student_list.html`.
