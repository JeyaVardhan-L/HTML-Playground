"""
build_report.py
Generates the comprehensive, academic WAF Final Lab Assignment report
covering Flask, Django, and SQLite, and converts it to PDF.
Author: Jeyavardhan Lekkala (2024009057)
"""

import os
import sys
import subprocess
from pathlib import Path

import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

DOCS_DIR = Path(__file__).resolve().parent
ROOT_DIR = DOCS_DIR.parent
SCREENSHOTS_DIR = DOCS_DIR / "screenshots"

COLOR_NAVY = "1B365D"
COLOR_SLATE = "2E75B6"
COLOR_CHARCOAL = "24292E"
COLOR_LIGHT_BG = "F6F8FA"
COLOR_BORDER = "D0D7DE"
COLOR_SUCCESS = "28A745"

RGB_NAVY = RGBColor(0x1B, 0x36, 0x5D)
RGB_SLATE = RGBColor(0x2E, 0x75, 0xB6)
RGB_CHARCOAL = RGBColor(0x24, 0x29, 0x2E)
RGB_MUTED = RGBColor(0x57, 0x60, 0x6A)


def set_cell_shading(cell, hex_color: str):
    tc_pr = cell._tc.get_or_add_tcPr()
    for s in tc_pr.findall(qn("w:shd")):
        tc_pr.remove(s)
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tc_pr.append(shd)


def set_cell_margins(cell, top: int = 120, bottom: int = 120, left: int = 160, right: int = 160):
    tc_pr = cell._tc.get_or_add_tcPr()
    for m in tc_pr.findall(qn("w:tcMar")):
        tc_pr.remove(m)
    tc_mar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tc_pr.append(tc_mar)


def set_table_borders(table, color="D0D7DE", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideV w:val="none"/>'
        f'<w:left w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)


def add_code_block(doc, code_text: str):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    cell = table.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_shading(cell, COLOR_LIGHT_BG)
    set_cell_margins(cell, top=140, bottom=140, left=180, right=180)
    
    # Border for code block
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="4" w:color="{COLOR_BORDER}"/>'
        f'<w:left w:val="single" w:sz="12" w:color="{COLOR_SLATE}"/>'
        f'<w:bottom w:val="single" w:sz="4" w:color="{COLOR_BORDER}"/>'
        f'<w:right w:val="single" w:sz="4" w:color="{COLOR_BORDER}"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(code_text.strip())
    run.font.name = "Consolas"
    run.font.size = Pt(8.5)
    run.font.color.rgb = RGB_CHARCOAL
    
    doc.add_paragraph().paragraph_format.space_after = Pt(4)


def add_image_evidence(doc, img_path: Path, caption: str, width_in=5.8):
    if not img_path.exists():
        p = doc.add_paragraph(f"[Image evidence missing: {img_path.name}]")
        p.runs[0].font.color.rgb = RGBColor(0xDC, 0x35, 0x45)
        return

    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(6)
    p_img.paragraph_format.space_after = Pt(4)
    run = p_img.add_run()
    run.add_picture(str(img_path), width=Inches(width_in))
    
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(2)
    p_cap.paragraph_format.space_after = Pt(12)
    run_cap = p_cap.add_run(f"Figure: {caption}")
    run_cap.font.name = "Arial"
    run_cap.font.size = Pt(9.0)
    run_cap.font.italic = True
    run_cap.font.color.rgb = RGB_MUTED


def build_report_doc():
    doc = Document()
    
    # Page Setup: A4, 0.75" margins
    section = doc.sections[0]
    section.page_width = Inches(8.27)
    section.page_height = Inches(11.69)
    section.top_margin = Inches(0.75)
    section.bottom_margin = Inches(0.75)
    section.left_margin = Inches(0.75)
    section.right_margin = Inches(0.75)
    
    # Header & Footer setup
    header = section.header
    hp = header.paragraphs[0]
    hp.text = "WAF Lab Final Assignment | Flask, Django, SQLite & GitHub"
    hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    hp.runs[0].font.size = Pt(8.5)
    hp.runs[0].font.color.rgb = RGB_MUTED
    
    footer = section.footer
    fp = footer.paragraphs[0]
    fp.text = "Student: Jeyavardhan Lekkala (2024009057)  •  GITAM Deemed to be University"
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    fp.runs[0].font.size = Pt(8.5)
    fp.runs[0].font.color.rgb = RGB_MUTED
    
    # ==================== COVER / HEADER BANNER ====================
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(10)
    title_p.paragraph_format.space_after = Pt(2)
    r_sub = title_p.add_run("DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING\nGITAM DEEMED TO BE UNIVERSITY\n")
    r_sub.font.name = "Arial"
    r_sub.font.size = Pt(10)
    r_sub.font.bold = True
    r_sub.font.color.rgb = RGB_SLATE

    r_title = title_p.add_run("Web Application Frameworks (WAF) Lab\nFinal Practical Assignment Report")
    r_title.font.name = "Arial"
    r_title.font.size = Pt(20)
    r_title.font.bold = True
    r_title.font.color.rgb = RGB_NAVY

    sub_p = doc.add_paragraph()
    sub_p.paragraph_format.space_after = Pt(12)
    r_sub2 = sub_p.add_run("Comparative Implementation of SQLite-Backed Web Applications using Flask and Django")
    r_sub2.font.name = "Arial"
    r_sub2.font.size = Pt(12)
    r_sub2.font.color.rgb = RGB_SLATE

    # Metadata Card Table
    meta_table = doc.add_table(rows=2, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_table.autofit = False
    
    meta_data = [
        ("Student Name:", "Jeyavardhan Lekkala", "Roll Number:", "2024009057"),
        ("Course / Lab:", "Web Application Frameworks (WAF)", "Submission Date:", "November 2026")
    ]
    for row_idx, row in enumerate(meta_table.rows):
        for cell_idx, cell in enumerate(row.cells):
            cell.width = Inches(3.25)
            set_cell_shading(cell, COLOR_LIGHT_BG)
            set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
            
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            
            if cell_idx == 0:
                lbl, val = meta_data[row_idx][0], meta_data[row_idx][1]
            else:
                lbl, val = meta_data[row_idx][2], meta_data[row_idx][3]
            
            r_l = p.add_run(lbl + " ")
            r_l.font.name = "Arial"
            r_l.font.size = Pt(9.5)
            r_l.font.bold = True
            r_l.font.color.rgb = RGB_NAVY
            
            r_v = p.add_run(val)
            r_v.font.name = "Arial"
            r_v.font.size = Pt(9.5)
            r_v.font.color.rgb = RGB_CHARCOAL

    set_table_borders(meta_table)
    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # ==================== 1. OBJECTIVES ====================
    h1 = doc.add_heading("1. Assignment Title & Objectives", level=1)
    h1.runs[0].font.color.rgb = RGB_NAVY
    h1.runs[0].font.size = Pt(14)
    h1.paragraph_format.space_before = Pt(12)
    h1.paragraph_format.space_after = Pt(4)

    p_obj = doc.add_paragraph(
        "The objective of this final practical assignment is to implement, test, document, and compare two "
        "independent Python web applications interacting with an embedded SQLite database: one built with the Flask "
        "micro-framework and the other with the Django full-stack framework. Specific goals include:"
    )
    p_obj.paragraph_format.space_after = Pt(4)
    
    bullets = [
        "Create a modular Flask application connecting directly to an SQLite database (`students.db`).",
        "Define an explicit `students` table, implement automated database seeding, and query records using native SQL.",
        "Create a structured Django project with a `Student` ORM model, schema migrations, and repeatable data seeding.",
        "Retrieve data through Django's Object-Relational Mapper (ORM) and present it in dynamic Django templates.",
        "Display equivalent student datasets across both frameworks with a clean, beginner-friendly UI for faculty review.",
        "Verify end-to-end functionality via automated testing and real browser screenshot capture.",
        "Submit the full implementation, documentation, and assets to GitHub using the Git CLI."
    ]
    for b in bullets:
        bp = doc.add_paragraph(style='List Bullet')
        bp.paragraph_format.space_before = Pt(0)
        bp.paragraph_format.space_after = Pt(2)
        r = bp.add_run(b)
        r.font.name = "Arial"
        r.font.size = Pt(10)

    # ==================== 2. SOFTWARE & TECHNOLOGIES ====================
    h2 = doc.add_heading("2. Software & Technologies Used", level=1)
    h2.runs[0].font.color.rgb = RGB_NAVY
    h2.runs[0].font.size = Pt(14)
    h2.paragraph_format.space_before = Pt(14)
    h2.paragraph_format.space_after = Pt(6)

    tech_table = doc.add_table(rows=7, cols=3)
    tech_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    tech_table.autofit = False
    
    headers = ["Component", "Technology / Tool", "Purpose in Practical"]
    for i, title in enumerate(headers):
        cell = tech_table.cell(0, i)
        cell.width = Inches(2.16)
        set_cell_shading(cell, COLOR_NAVY)
        set_cell_margins(cell, top=100, bottom=100, left=140, right=140)
        p = cell.paragraphs[0]
        r = p.add_run(title)
        r.font.name = "Arial"
        r.font.size = Pt(9.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    tech_rows = [
        ("Programming Language", "Python 3.14.6", "Core backend application programming language"),
        ("Micro-Framework", "Flask 3.1.3", "Lightweight routing, request dispatching, and Jinja2 templating"),
        ("Full-Stack Framework", "Django 6.1.2", "MVT framework providing ORM, migrations, and template rendering"),
        ("Embedded Database", "SQLite 3", "Self-contained serverless relational database engine (`.db` files)"),
        ("Browser Automation", "Playwright 1.64.1 (Chromium)", "End-to-end verification and high-resolution screenshot evidence capture"),
        ("Version Control", "Git CLI & GitHub", "Repository tracking, commit structuring, and remote push submission")
    ]
    for row_idx, data in enumerate(tech_rows, start=1):
        for col_idx, text in enumerate(data):
            cell = tech_table.cell(row_idx, col_idx)
            cell.width = Inches(2.16)
            set_cell_shading(cell, COLOR_LIGHT_BG if row_idx % 2 == 1 else "FFFFFF")
            set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(text)
            r.font.name = "Arial"
            r.font.size = Pt(9.0)
            if col_idx == 0:
                r.font.bold = True

    set_table_borders(tech_table)
    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # ==================== 3. FLASK APPLICATION ====================
    h3 = doc.add_heading("3. Flask Application with SQLite", level=1)
    h3.runs[0].font.color.rgb = RGB_NAVY
    h3.runs[0].font.size = Pt(14)
    h3.paragraph_format.space_before = Pt(14)
    h3.paragraph_format.space_after = Pt(4)

    p_flask_desc = doc.add_paragraph(
        "Flask is a minimalist WSGI micro-framework that gives developers direct control over database interactions. "
        "In this implementation, the native Python `sqlite3` standard library is used without an external ORM. "
        "The application maintains its own dedicated database file (`students.db`), checks and initializes the "
        "`students` table upon startup, executes explicit SQL queries, and passes data to a Jinja2 template."
    )
    p_flask_desc.paragraph_format.space_after = Pt(6)

    doc.add_heading("Folder Structure:", level=2).runs[0].font.color.rgb = RGB_SLATE
    add_code_block(doc, 
"""flask-app/
├── app.py                # Flask application, SQLite schema setup & route handler
├── requirements.txt      # Dependency declaration (Flask>=3.0.0)
├── README.md             # Execution commands and architecture notes
├── students.db           # SQLite database file containing the 'students' table
└── templates/
    └── index.html        # Jinja2 template rendering the student table""")

    doc.add_heading("Database Connection & Initialization Logic:", level=2).runs[0].font.color.rgb = RGB_SLATE
    p_db_exp = doc.add_paragraph(
        "The application configures `conn.row_factory = sqlite3.Row` so retrieved database tuples can be accessed "
        "like Python dictionaries using column names (`student['name']`). Automatic initialization is triggered upon import:"
    )
    p_db_exp.paragraph_format.space_after = Pt(4)

    add_code_block(doc,
"""def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            year TEXT NOT NULL
        )
    ''')
    cursor.execute("SELECT COUNT(*) FROM students")
    if cursor.fetchone()[0] == 0:
        sample_students = [
            ("Jeyavardhan Lekkala", "Computer Science & Engineering", "3rd Year"),
            ("Sarah Jenkins", "Information Technology", "3rd Year"),
            ("Rahul Sharma", "Computer Science & Engineering", "2nd Year"),
            ("Priya Patel", "Electronics & Communication", "4th Year"),
            ("Alex Rivera", "Mechanical Engineering", "1st Year"),
        ]
        cursor.executemany("INSERT INTO students (name, department, year) VALUES (?, ?, ?)", sample_students)
        conn.commit()
    conn.close()""")

    doc.add_heading("Route Handler & Template Rendering:", level=2).runs[0].font.color.rgb = RGB_SLATE
    p_route_exp = doc.add_paragraph(
        "When a client requests the root endpoint (`GET /`), Flask opens a database connection, performs a `SELECT` "
        "query, and renders `index.html` passing the row collection:"
    )
    p_route_exp.paragraph_format.space_after = Pt(4)

    add_code_block(doc,
"""@app.route("/")
def index():
    conn = get_db_connection()
    students = conn.execute("SELECT id, name, department, year FROM students ORDER BY id ASC").fetchall()
    conn.close()
    return render_template("index.html", students=students)""")

    doc.add_heading("Flask Application Output Screenshot:", level=2).runs[0].font.color.rgb = RGB_SLATE
    add_image_evidence(
        doc,
        SCREENSHOTS_DIR / "flask_student_records.png",
        "Flask web application running on http://127.0.0.1:5001 displaying dynamic records from SQLite3"
    )

    # ==================== 4. DJANGO APPLICATION ====================
    h4 = doc.add_heading("4. Django Application with SQLite", level=1)
    h4.runs[0].font.color.rgb = RGB_NAVY
    h4.runs[0].font.size = Pt(14)
    h4.paragraph_format.space_before = Pt(14)
    h4.paragraph_format.space_after = Pt(4)

    p_dj_desc = doc.add_paragraph(
        "Django follows the Model-View-Template (MVT) pattern with a batteries-included philosophy. "
        "Instead of writing raw SQL statements, developers declare Python model classes. Django's migration engine "
        "automatically translates these Python classes into SQLite table definitions (`students_student`). "
        "Queries are executed via Django's high-level Object-Relational Mapper (ORM)."
    )
    p_dj_desc.paragraph_format.space_after = Pt(6)

    doc.add_heading("Folder Structure:", level=2).runs[0].font.color.rgb = RGB_SLATE
    add_code_block(doc,
"""django-app/
├── manage.py                     # Django CLI command orchestrator
├── requirements.txt              # Dependency declaration (Django>=5.0.0)
├── README.md                     # Setup, migration, and run commands
├── db.sqlite3                    # Django SQLite database
├── student_portal/               # Project configuration package
│   ├── settings.py               # Database engine, INSTALLED_APPS & middleware
│   └── urls.py                   # Master URL routing table
└── students/                     # Application package
    ├── models.py                 # Student model class definition
    ├── views.py                  # View function executing Student.objects.all()
    ├── urls.py                   # Application route mapping ('' -> student_list)
    ├── migrations/
    │   └── 0001_initial.py       # Auto-generated initial database migration
    ├── management/commands/
    │   └── seed_students.py      # Repeatable CLI database seeder command
    └── templates/students/
        └── student_list.html     # Django template with {% for student in students %}""")

    doc.add_heading("Model Definition & Migrations:", level=2).runs[0].font.color.rgb = RGB_SLATE
    p_m_exp = doc.add_paragraph(
        "The `Student` model is declared in `students/models.py`. Running `makemigrations` creates migration file "
        "`0001_initial.py`, and `migrate` executes the corresponding DDL against `db.sqlite3`:"
    )
    p_m_exp.paragraph_format.space_after = Pt(4)

    add_code_block(doc,
"""class Student(models.Model):
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    year = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.id} - {self.name} ({self.department})"
""")

    doc.add_heading("ORM Data Retrieval & Repeatable Seeding:", level=2).runs[0].font.color.rgb = RGB_SLATE
    p_orm_exp = doc.add_paragraph(
        "Data retrieval is abstracted through the ORM call `Student.objects.all().order_by('id')`. "
        "A repeatable custom management command (`python manage.py seed_students`) and an on-demand fallback in "
        "`views.py` guarantee that faculty running the project always see populated student records:"
    )
    p_orm_exp.paragraph_format.space_after = Pt(4)

    add_code_block(doc,
"""def student_list(request):
    if not Student.objects.exists():
        sample_students = [
            {"name": "Jeyavardhan Lekkala", "department": "Computer Science & Engineering", "year": "3rd Year"},
            {"name": "Sarah Jenkins", "department": "Information Technology", "year": "3rd Year"},
            {"name": "Rahul Sharma", "department": "Computer Science & Engineering", "year": "2nd Year"},
            {"name": "Priya Patel", "department": "Electronics & Communication", "year": "4th Year"},
            {"name": "Alex Rivera", "department": "Mechanical Engineering", "year": "1st Year"},
        ]
        Student.objects.bulk_create([Student(**s) for s in sample_students])

    students = Student.objects.all().order_by('id')
    return render(request, 'students/student_list.html', {'students': students})""")

    doc.add_heading("Django Application Output Screenshot:", level=2).runs[0].font.color.rgb = RGB_SLATE
    add_image_evidence(
        doc,
        SCREENSHOTS_DIR / "django_student_records.png",
        "Django web application running on http://127.0.0.1:8001 displaying records queried via Django ORM"
    )

    # ==================== 5. STEPS TO RUN ====================
    h5 = doc.add_heading("5. Steps to Run Both Applications", level=1)
    h5.runs[0].font.color.rgb = RGB_NAVY
    h5.runs[0].font.size = Pt(14)
    h5.paragraph_format.space_before = Pt(14)
    h5.paragraph_format.space_after = Pt(4)

    doc.add_heading("How to Run the Flask Application:", level=2).runs[0].font.color.rgb = RGB_SLATE
    flask_steps = (
        "1. Open a terminal and navigate to: cd Assignment-8/flask-app\n"
        "2. Install requirements: pip install -r requirements.txt\n"
        "3. Start Flask server: python app.py\n"
        "4. Open browser at: http://127.0.0.1:5000/\n"
        "   (The database students.db is automatically initialized and populated on startup.)"
    )
    add_code_block(doc, flask_steps)

    doc.add_heading("How to Run the Django Application:", level=2).runs[0].font.color.rgb = RGB_SLATE
    django_steps = (
        "1. Open a terminal and navigate to: cd Assignment-8/django-app\n"
        "2. Install requirements: pip install -r requirements.txt\n"
        "3. Apply database migrations: python manage.py migrate\n"
        "4. Seed sample records (optional / repeatable): python manage.py seed_students\n"
        "5. Start Django development server: python manage.py runserver 8000\n"
        "6. Open browser at: http://127.0.0.1:8000/"
    )
    add_code_block(doc, django_steps)

    # ==================== 6. TESTING & RESULTS ====================
    h6 = doc.add_heading("6. Testing and Verification Results", level=1)
    h6.runs[0].font.color.rgb = RGB_NAVY
    h6.runs[0].font.size = Pt(14)
    h6.paragraph_format.space_before = Pt(14)
    h6.paragraph_format.space_after = Pt(6)

    test_table = doc.add_table(rows=10, cols=4)
    test_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    test_table.autofit = False

    test_headers = ["Framework", "Test Verification Item", "Observed Result", "Status"]
    col_widths = [Inches(1.2), Inches(2.6), Inches(1.9), Inches(0.8)]
    for i, title in enumerate(test_headers):
        cell = test_table.cell(0, i)
        cell.width = col_widths[i]
        set_cell_shading(cell, COLOR_NAVY)
        set_cell_margins(cell, top=100, bottom=100, left=140, right=140)
        p = cell.paragraphs[0]
        r = p.add_run(title)
        r.font.name = "Arial"
        r.font.size = Pt(9.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    test_rows = [
        ("Flask", "Server startup on port 5000 / 5001", "WSGI server active, listening without errors", "PASS"),
        ("Flask", "SQLite database and table creation", "students.db created; table 'students' established", "PASS"),
        ("Flask", "Sample record initialization", "5 records inserted via parameterized cursor", "PASS"),
        ("Flask", "Data retrieval via cursor", "SELECT query returned 5 dictionary-like Row records", "PASS"),
        ("Flask", "HTML Jinja2 rendering", "HTTP 200; student names & department pills rendered", "PASS"),
        ("Django", "Project & app startup", "Django 6.1.2 configuration loaded without warnings", "PASS"),
        ("Django", "Migrations execution", "makemigrations generated 0001; migrate created tables", "PASS"),
        ("Django", "Repeatable seeding (seed_students)", "Command executed successfully; 5 student objects created", "PASS"),
        ("Django", "ORM data retrieval & template", "Student.objects.all() returned records; HTTP 200 rendered", "PASS"),
    ]

    for row_idx, data in enumerate(test_rows, start=1):
        for col_idx, text in enumerate(data):
            cell = test_table.cell(row_idx, col_idx)
            cell.width = col_widths[col_idx]
            set_cell_shading(cell, COLOR_LIGHT_BG if row_idx % 2 == 1 else "FFFFFF")
            set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(text)
            r.font.name = "Arial"
            r.font.size = Pt(9.0)
            if col_idx == 3:
                r.font.bold = True
                r.font.color.rgb = RGBColor(0x28, 0xA7, 0x45)

    set_table_borders(test_table)
    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # ==================== 7. CONCLUSION ====================
    h7 = doc.add_heading("7. Comparative Analysis & Conclusion", level=1)
    h7.runs[0].font.color.rgb = RGB_NAVY
    h7.runs[0].font.size = Pt(14)
    h7.paragraph_format.space_before = Pt(14)
    h7.paragraph_format.space_after = Pt(4)

    p_conc = doc.add_paragraph(
        "This assignment demonstrated two distinct architectural paradigms in Python web development for database-backed applications:\n\n"
        "1. Flask (Micro-Framework Approach): Offers minimal overhead and gives the developer total freedom. "
        "The developer is responsible for manually establishing the SQLite connection, managing cursor lifecycles, writing "
        "SQL queries, and handling migrations. This simplicity makes Flask ideal for lightweight utilities, microservices, "
        "and beginner learning.\n\n"
        "2. Django (Full-Stack MVT Approach): Offers a robust, standardized architecture with built-in migrations, an "
        "expressive Object-Relational Mapper (ORM), admin dashboard capabilities, and secure defaults. While it involves "
        "more boilerplate configuration initially, it eliminates raw SQL syntax errors and provides scalable data modeling.\n\n"
        "Both applications successfully fulfilled all requirements: establishing separate SQLite databases, automatically "
        "initializing equivalent student records, dynamically querying and rendering the data, and proving end-to-end "
        "isolation and reproducibility."
    )
    p_conc.paragraph_format.space_after = Pt(12)

    # Output path
    docx_output = DOCS_DIR / "WAF_Final_Assignment_Flask_Django_SQLite.docx"
    doc.save(str(docx_output))
    print(f">>> Generated DOCX document: {docx_output}")
    return docx_output


def convert_docx_to_pdf(docx_path: Path):
    pdf_path = docx_path.with_suffix(".pdf")
    docx_abs = str(docx_path.resolve())
    pdf_abs = str(pdf_path.resolve())

    print(f">>> Converting {docx_path.name} to PDF via Microsoft Word COM...")
    ps_script = f"""
$ErrorActionPreference = "Stop"
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
try {{
    $doc = $word.Documents.Open("{docx_abs}")
    $doc.SaveAs([ref]"{pdf_abs}", [ref]17)
    $doc.Close([ref]0)
    Write-Host "RENDER_PDF_SUCCESS"
}} catch {{
    Write-Error $_
    exit 1
}} finally {{
    $word.Quit()
}}
"""
    res = subprocess.run(["powershell", "-NoProfile", "-Command", ps_script], capture_output=True, text=True)
    if res.returncode == 0 and "RENDER_PDF_SUCCESS" in res.stdout:
        print(f">>> Successfully generated PDF: {pdf_path}")
        return pdf_path
    else:
        print(f">>> PDF conversion warning: {res.stderr or res.stdout}")
        return None


if __name__ == "__main__":
    docx_file = build_report_doc()
    convert_docx_to_pdf(docx_file)
