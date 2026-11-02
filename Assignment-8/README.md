# Web Application Frameworks (WAF) Lab — Assignment 8
## Comparative SQLite Applications: Flask vs. Django

**Subject:** Web Application Frameworks (WAF) Lab  
**Student Name:** Jeyavardhan Lekkala  
**Roll Number:** 2024009057  
**Department:** Department of Computer Science & Engineering  
**Institution:** GITAM Deemed to be University  

---

## 1. Directory Structure

```text
Assignment-8/
├── README.md                      # Assignment overview and navigation
├── capture_evidence.py            # Playwright script to capture live screenshots
├── flask-app/                     # Flask + SQLite web application
│   ├── app.py                     # Main application script & database logic
│   ├── requirements.txt           # Flask dependencies
│   ├── README.md                  # Flask installation & run guide
│   └── templates/
│       └── index.html             # Jinja2 template rendering student records
├── django-app/                    # Django + SQLite web application
│   ├── manage.py                  # Django CLI manager
│   ├── requirements.txt           # Django dependencies
│   ├── README.md                  # Django installation & run guide
│   ├── student_portal/            # Project configuration package
│   │   ├── settings.py            # Django configuration
│   │   ├── urls.py                # Main URL router
│   │   ├── wsgi.py
│   │   └── asgi.py
│   └── students/                  # Students application
│       ├── models.py              # Student ORM model definition
│       ├── views.py               # View function retrieving data via ORM
│       ├── urls.py                # App URL routing
│       ├── migrations/            # Django database migrations
│       │   └── 0001_initial.py
│       ├── management/commands/   # Custom management commands
│       │   └── seed_students.py   # Repeatable database seeding command
│       └── templates/students/
│           └── student_list.html  # Django template rendering student records
└── documentation/                 # Submission documentation
    ├── REPORT.md                  # Complete markdown report
    ├── build_report.py            # Script compiling DOCX and PDF documents
    ├── WAF_Final_Assignment_Flask_Django_SQLite.docx # Word document report
    ├── WAF_Final_Assignment_Flask_Django_SQLite.pdf  # Academic PDF report
    └── screenshots/               # Actual live evidence screenshots
        ├── flask_student_records.png
        └── django_student_records.png
```

---

## 2. Quick Start Guides

### Running the Flask Application
```bash
cd flask-app
pip install -r requirements.txt
python app.py
```
Visit `http://127.0.0.1:5000/` in your browser.

### Running the Django Application
```bash
cd django-app
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_students
python manage.py runserver 8000
```
Visit `http://127.0.0.1:8000/` in your browser.

---

## 3. Assignment Documentation

- **Word Document:** [`documentation/WAF_Final_Assignment_Flask_Django_SQLite.docx`](file:///c:/Users/user/Downloads/HTML-Playground/HTML-Playground/Assignment-8/documentation/WAF_Final_Assignment_Flask_Django_SQLite.docx)
- **PDF Report:** [`documentation/WAF_Final_Assignment_Flask_Django_SQLite.pdf`](file:///c:/Users/user/Downloads/HTML-Playground/HTML-Playground/Assignment-8/documentation/WAF_Final_Assignment_Flask_Django_SQLite.pdf)
- **Markdown Report:** [`documentation/REPORT.md`](file:///c:/Users/user/Downloads/HTML-Playground/HTML-Playground/Assignment-8/documentation/REPORT.md)
