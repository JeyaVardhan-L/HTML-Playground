# WAF Automated Lab Report Generator

A reusable, fully automated academic lab report generator for the **Web Application Frameworks (WAF) Lab** repository.

## Capabilities

Given an assignment number (e.g., Assignment 2), the generator automatically:
1. **Locates** the assignment directory and resolves all source code files.
2. **Launches** the assignment application on an isolated, ephemeral port.
3. **Polls** until the application is ready and responsive.
4. **Executes** non-destructive Playwright browser automation with real Chromium (Desktop & Mobile viewports).
5. **Demonstrates** key features (DOM interactions, form validation, real-time search, iframe navigation).
6. **Captures** high-resolution (device scale factor 2.0) evidence screenshots.
7. **Compiles** a single, comprehensive, academic-standard Microsoft Word document (`.docx`) including:
   - Official university cover page with editable student details
   - Aim & objectives
   - Software and hardware requirements
   - Faculty requirements compliance mapping table
   - Architectural implementation procedure
   - Experimental evidence with captions and detailed technical explanations
   - Academic result and conclusion
   - Viva-voce questions and answers
   - Complete unabridged source code appendix
8. **Terminates** strictly only the server processes started by the generator.
9. **Saves** the final report in `reports/Assignment-{N}/WAF_Assignment_{N}.docx`.

---

## Directory Architecture

```text
tools/lab-report-generator/
├── config.py             # Assignment metadata registry, source file specs, and browser scenes
├── server_manager.py     # Port discovery, subprocess lifecycle, and safe process termination
├── browser_runner.py     # Playwright Chromium automation, action executor, and screenshot capture
├── doc_builder.py        # python-docx builder formatting academic lab records and code appendices
├── generate.py           # Master CLI entry point
├── run.py                # Wrapper auto-routing to project-local .venv python
├── requirements.txt      # Python dependencies (playwright, python-docx, pillow)
└── README.md             # Documentation
```

---

## Quick Start / How to Run

### Option 1: PowerShell Script (Fastest on Windows)
```powershell
# Generate report for Assignment 2
.\Generate-LabReport.ps1 -Assignment 2

# Or specify custom student details
.\Generate-LabReport.ps1 -Assignment 2 -StudentName "Jey" -RollNo "9057"
```

### Option 2: npm Script
```powershell
npm run lab-report -- --assignment 2
```

### Option 3: Python CLI Directly
```powershell
# Using the local virtual environment
tools\lab-report-generator\.venv\Scripts\python.exe tools/lab-report-generator/generate.py --assignment 2

# Or using the run wrapper with system python
python tools/lab-report-generator/run.py --assignment 2
```

---

## Output Location

Generated reports and screenshot evidence are saved in:
```text
reports/
└── Assignment-2/
    ├── WAF_Assignment_2.docx        ← Final editable Microsoft Word lab record
    └── screenshots/                 ← High-resolution output captures
        ├── 01_parent_shell_home.png
        ├── 02_models_explorer_table.png
        ├── 03_models_search_interaction.png
        ├── 04_developer_survey_initial.png
        ├── 05_developer_survey_submitted.png
        ├── 06_semantic_articles_view.png
        ├── 07_resources_and_compliance.png
        ├── 08_mobile_responsive_view.png
        └── 09_standalone_banner_detection.png
```

---

## Extending for Future Assignments (3, 4, 5, 6, 7)

To add support for a new assignment, add an `AssignmentConfig` entry to `ASSIGNMENT_REGISTRY` in `tools/lab-report-generator/config.py`:

```python
ASSIGNMENT_REGISTRY[3] = AssignmentConfig(
    assignment_id=3,
    folder_name="Assignment-3",
    title="Lab Assignment 3: JavaScript Foundations & DOM",
    subtitle="Core JavaScript Practicals & DHTML Interactions",
    aim="...",
    server_type="static_http",  # or "express" for Assignment 4/5/6
    default_port=8000,
    entry_url="/practical-1-form.html",
    source_files=[...],
    scenes=[...],
    viva_questions=[...],
    conclusion="..."
)
```

For Node/Express assignments (Assignments 4, 5, 6):
- Set `server_type="express"`
- Set `server_command=["node", "server.js"]` (or custom script)
- Define corresponding Playwright test scenes.
