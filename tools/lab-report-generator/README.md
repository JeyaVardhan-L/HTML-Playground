# WAF Automated Lab Report Generator

A reusable, fully automated academic lab report generator for the **Web Application Frameworks (WAF) Lab** repository. Produces both publication-grade editable Microsoft Word documents (`.docx`) and pixel-accurate Portable Document Format (`.pdf`) reports adhering strictly to university lab record standards.

---

## Key Capabilities

Given an assignment number (e.g., Assignment 2), the generator automatically:
1. **Locates** the assignment directory and resolves all source code files.
2. **Launches** the assignment application on an isolated, ephemeral port.
3. **Polls** until the application is ready and responsive.
4. **Executes** non-destructive Playwright browser automation with real Chromium (Desktop & Mobile viewports).
5. **Demonstrates** key features (DOM interactions, form validation, real-time search, iframe navigation).
6. **Captures** high-resolution (device scale factor 2.0) evidence screenshots.
7. **Compiles** an academic-standard Microsoft Word document (`.docx`) into a staging area including:
   - Official university cover page with editable student details and balanced vertical geometry.
   - Aim & objectives.
   - Software and hardware requirements.
   - Faculty requirements compliance mapping table (with repeating headers).
   - Architectural implementation procedure.
   - Experimental evidence with tight component bonding, aspect-ratio bounding boxes, and detailed technical explanations.
   - Academic result and conclusion.
   - Viva-voce study guide questions and answers.
   - Complete unabridged source code appendix with hanging indents, clean monospace typography, and line numbers.
8. **Converts** the staged Word document directly to PDF via local Microsoft Word COM automation, ensuring 100% pagination fidelity.
9. **Renders** all PDF pages to high-resolution PNG preview images (150 DPI) using `pypdfium2`.
10. **Executes** an automated 14-point Quality Assurance (QA) audit to detect empty pages, broken images, unbonded headings, missing sections, and code truncation.
11. **Performs** atomic replacement of final outputs only after all quality checks pass, ensuring pre-existing reports are never corrupted or left stale.

---

## Directory Architecture

```text
tools/lab-report-generator/
├── config.py             # Assignment metadata registry, source file specs, and browser scenes
├── server_manager.py     # Port discovery, subprocess lifecycle, and safe process termination
├── browser_runner.py     # Playwright Chromium automation, action executor, and screenshot capture
├── doc_builder.py        # python-docx builder formatting academic lab records and code appendices
├── render_docx.py        # Microsoft Word COM PDF converter and pypdfium2 page image exporter
├── qa_checker.py         # Automated Quality Assurance (QA) validation engine
├── generate.py           # Master CLI orchestrator (staging, execution, QA, atomic replacement)
├── run.py                # Wrapper auto-routing to project-local .venv python
├── requirements.txt      # Python dependencies (playwright, python-docx, pillow, pypdfium2)
└── README.md             # Documentation & troubleshooting guide
```

---

## Quick Start / How to Run

### Option 1: PowerShell Entry Point (Recommended on Windows)
```powershell
# Generate report for Assignment 2
.\Generate-LabReport.ps1 -Assignment 2

# Or specify custom student details
.\Generate-LabReport.ps1 -Assignment 2 -StudentName "Jey" -RollNo "9057"
```

### Option 2: npm Script
```powershell
npm run lab-report -- --assignment 2
# Or direct assignment shortcut
npm run report:2
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

Generated reports, screenshot evidence, and preview page images are saved in:
```text
reports/
└── Assignment-2/
    ├── WAF_Assignment_2.docx        ← Final editable Microsoft Word lab record
    ├── WAF_Assignment_2.pdf         ← Final native Microsoft Word PDF report
    ├── preview_pages/               ← 150 DPI rendered PNG pages for visual QA
    │   ├── page_01.png
    │   ├── ...
    │   └── page_36.png
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

## Quality Assurance (QA) Engine

The generator executes an automated validation engine (`qa_checker.py`) before overwriting any report:

| Category | Test Name | Validation Rule |
| :--- | :--- | :--- |
| **Integrity** | DOCX Existence & Size | DOCX exists and size >= 50 KB. |
| **Integrity** | PDF Existence & Size | PDF exists and size >= 50 KB. |
| **Screenshots** | Image File Availability | All configured screenshot files exist on disk. |
| **Screenshots** | Image Dimensions | Images are >= 200px (not clipped or corrupt). |
| **Screenshots** | Embedded Media Parts | Images are embedded in DOCX package (`/word/media/`). |
| **Structure** | Required Academic Sections | Sections 1 through 8 are present in heading hierarchy. |
| **Structure** | Heading Orphan Prevention | `keep_with_next = True` on all heading paragraphs. |
| **Tables** | Repeating Headers | Multi-page tables include `w:tblHeader` on row 0. |
| **Tables** | Row Split Prevention | Table rows enforce `w:cantSplit` across breaks. |
| **Pagination** | First Page Suppression | Cover page suppresses running header and footer. |
| **Pagination** | Dynamic Page Numbering | Footer contains dynamic `PAGE` and `NUMPAGES` fields. |
| **Appendix** | Source Code Completeness | All source files are present in the appendix. |
| **Visual QA** | Total Document Page Count | Minimum expected page threshold met. |
| **Visual QA** | Blank Page Detection | Pixel inspection detects accidental blank content pages (>98% white). |

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

For Node/Express assignments (Assignments 4, 5, 6, 7):
- Set `server_type="express"`
- Set `server_command=["node", "server.js"]` (or custom script)
- Define corresponding Playwright test scenes.

---

## Troubleshooting Guide

### 1. Microsoft Word COM Conversion (`render_docx.py`)
- **Requirement:** Microsoft Word 2016, 2019, 2021, or Microsoft 365 must be installed locally.
- **Symptom:** `Microsoft Word PDF conversion failed: ...`
- **Solution:** Ensure Word is installed and activated. Close any modal dialogs or background Word instances using `Stop-Process -Name WINWORD -Force` in PowerShell.

### 2. Port In Use / Server Conflicts
- **Symptom:** `Port 8000 is occupied by an external process.`
- **Solution:** The generator automatically detects occupied ports and chooses the next free port. You can also specify `-Port 8080` manually.

### 3. Missing Dependencies
- **Symptom:** `ModuleNotFoundError: No module named 'pypdfium2'` or `'playwright'`
- **Solution:** Activate the local virtual environment and install dependencies:
  ```powershell
  tools\lab-report-generator\.venv\Scripts\Activate.ps1
  pip install -r tools\lab-report-generator\requirements.txt
  playwright install chromium
  ```
