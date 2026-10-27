# WAF Automated Lab Report Generator

A reusable, fully automated academic lab report generator for the **Web Application Frameworks (WAF) Lab** repository. Produces publication-grade editable Microsoft Word documents (`.docx`) and pixel-accurate Portable Document Format (`.pdf`) reports adhering strictly to university academic lab record standards.

---

## Supported Assignments & Execution Matrix

Every assignment in this repository (Assignments 1 through 7) is fully configured and supported:

| Assignment | Title / Architecture | Execution Type | Server / CLI Entry | Port | Evidence Captured | Pages |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Assignment 1** | MVC Architecture Implementation | `express` | `node app.js` | 3000 | 1 Browser View (MVC View Engine) | 6 |
| **Assignment 2** | Minimalist Grayscale Interface (Mac UI) | `static_http` | Python HTTP Server | 8000 | 9 Browser Views (Desktop & Mobile) | 31 |
| **Assignment 3** | Core JavaScript Practicals Suite | `static_http` | Python HTTP Server | 8000 | 4 Browser Views (DOM & Events) | 32 |
| **Assignment 4** | Express Fetch & Core React Suite | `express` | `node server.js` + `npx vite build` | 3000 | 1 Browser View + 1 Terminal Card | 24 |
| **Assignment 5** | Fetch with Express & Request Counter | `express` | `node server.js` | 3001 | 3 Browser Views (Counter Increments) | 12 |
| **Assignment 6** | MongoDB Lookup, Aggregations & Express | `express` | `node api/server.js` + MongoDB Scripts | 3002 | 2 Browser Views + 5 Terminal Cards | 21 |
| **Assignment 7** | MongoDB Queries, Cursors & Atomic Updates | `none` | MongoDB CLI Scripts | N/A | 6 Terminal Evidence Cards | 19 |

---

## Key Capabilities

Given an assignment number (`1` through `7`), the generator automatically:
1. **Locates** the assignment directory and statically verifies all source code files.
2. **Executes** real CLI scripts and build steps (Node.js, Vite, MongoDB), capturing outputs and rendering high-DPI terminal cards.
3. **Launches** the assignment application on an isolated, ephemeral port (if a server is required).
4. **Polls** until the application is ready and responsive using bounded exponential backoff.
5. **Executes** non-destructive Playwright browser automation with real Chromium (Desktop & Mobile viewports).
6. **Demonstrates** key features (DOM interactions, form validation, real-time search, counter increments, API payloads).
7. **Captures** high-resolution (device scale factor 2.0) evidence screenshots and dark-mode terminal cards.
8. **Compiles** an academic-standard Microsoft Word document (`.docx`) into an isolated `.stage` directory:
   - Official university cover page with editable student details and balanced vertical geometry.
   - Section 1: Aim & Objectives.
   - Section 2: Software and Hardware Requirements.
   - Section 3: Faculty Requirements Compliance Mapping Table (with repeating headers `w:tblHeader`).
   - Section 4: Architectural Implementation Procedure.
   - Section 5: Experimental Evidence with tight component bonding, aspect-ratio bounding boxes, and detailed technical explanations.
   - Section 6: Academic Result and Conclusion.
   - Section 7: Viva-Voce Study Guide Questions and Answers.
   - Section 8: Unabridged Source Code Appendix with hanging indents, clean monospace typography, line numbers, and no accidental blank pages.
9. **Converts** the staged Word document directly to PDF via local Microsoft Word COM automation, ensuring 100% pagination fidelity.
10. **Renders** all PDF pages to high-resolution PNG preview images (150 DPI) using `pypdfium2`.
11. **Executes** an automated 14-point Quality Assurance (QA) audit detecting empty pages, broken images, unbonded headings, missing sections, and code truncation.
12. **Performs** atomic replacement of final outputs only after all quality checks pass. If any check fails, the pre-existing report is preserved and the failed stage is preserved in `.failed_stage` for inspection.

---

## Directory Architecture

```text
tools/lab-report-generator/
├── config.py             # Assignment metadata registry, source file specs, scenes & CLI specs (1-7)
├── cli_runner.py         # Subprocess runner & Playwright high-DPI terminal card generator
├── server_manager.py     # Port discovery, subprocess lifecycle, and safe process termination
├── browser_runner.py     # Playwright Chromium automation, action executor, and screenshot capture
├── doc_builder.py        # python-docx builder formatting academic lab records and code appendices
├── render_docx.py        # Microsoft Word COM PDF converter and pypdfium2 page image exporter
├── qa_checker.py         # Automated Quality Assurance (QA) 14-point validation engine
├── generate.py           # Master CLI orchestrator (staging, execution, QA, atomic replacement)
├── run.py                # Wrapper auto-routing to project-local .venv python
├── requirements.txt      # Python dependencies (playwright, python-docx, pillow, pypdfium2)
└── README.md             # Documentation & troubleshooting guide
```

---

## Quick Start / How to Run

### Option 1: PowerShell Entry Point (Recommended on Windows)

```powershell
# List all supported assignments and configuration status
.\Generate-LabReport.ps1 -List

# Validate configurations and source file presence on disk without generating
.\Generate-LabReport.ps1 -ValidateOnly

# Generate report for any assignment (1 through 7)
.\Generate-LabReport.ps1 -Assignment 2
.\Generate-LabReport.ps1 -Assignment 3
.\Generate-LabReport.ps1 -Assignment 4
.\Generate-LabReport.ps1 -Assignment 6

# Specify custom student details
.\Generate-LabReport.ps1 -Assignment 2 -StudentName "Your Name" -RollNo "12345"

# Evidence-only mode (captures screenshots and CLI cards without building DOCX/PDF)
.\Generate-LabReport.ps1 -Assignment 3 -EvidenceOnly

# Skip PDF rendering (useful if Microsoft Word is not installed)
.\Generate-LabReport.ps1 -Assignment 2 -SkipRender
```

### Option 2: npm Scripts

```powershell
# List supported assignments
npm run report:list

# Validate all assignment configurations
npm run report:validate

# Direct assignment shortcuts
npm run report:1
npm run report:2
npm run report:3
npm run report:4
npm run report:5
npm run report:6
npm run report:7

# Generic CLI interface
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

## Output Structure & Safe Atomic Replacement

All generated files are stored in `reports/Assignment-<N>/`:

```text
reports/
└── Assignment-<N>/
    ├── WAF_Assignment_<N>.docx        ← Final editable Microsoft Word lab record
    ├── WAF_Assignment_<N>.pdf         ← Final native Microsoft Word PDF report
    ├── preview_pages/                 ← 150 DPI rendered PNG pages for visual QA
    │   ├── page_01.png
    │   ├── page_02.png
    │   └── ...
    └── screenshots/                   ← High-resolution output captures & CLI cards
        ├── 01_scene_name.png
        └── 02_cli_command.png
```

### Safe Staging Protocol:
1. Files are built in an isolated `.stage` directory (`reports/Assignment-<N>/.stage`).
2. The 14-point QA audit evaluates the staged `.docx`, `.pdf`, screenshots, and rendered preview pages.
3. If **all 14 checks pass**, the stage files atomically replace the production report.
4. If **any check fails**, the production report is untouched, and the staging folder is preserved as `.failed_stage` with a detailed error log.

---

## Quality Assurance (QA) Engine

The generator executes an automated validation engine (`qa_checker.py`) verifying 14 distinct criteria before overwriting any report:

| # | Category | Test Name | Validation Rule |
| :-: | :--- | :--- | :--- |
| 1 | **Integrity** | DOCX Existence & Size | DOCX exists and size >= 50 KB. |
| 2 | **Integrity** | PDF Existence & Size | PDF exists and size >= 50 KB. |
| 3 | **Screenshots** | Image File Availability | All configured screenshot & CLI card files exist on disk. |
| 4 | **Screenshots** | Image Dimensions | Images are >= 200px width/height (not clipped or corrupt). |
| 5 | **Screenshots** | Embedded Media Parts | Images are embedded in DOCX drawing blips (`.//a:blip`). |
| 6 | **Structure** | Required Academic Sections | Sections 1 through 8 are present in heading hierarchy. |
| 7 | **Structure** | Heading Orphan Prevention | `keep_with_next = True` on all heading paragraphs. |
| 8 | **Tables** | Repeating Headers | Multi-page tables include `w:tblHeader` on row 0. |
| 9 | **Tables** | Row Split Prevention | Table rows enforce `w:cantSplit` across breaks. |
| 10 | **Pagination** | First Page Suppression | Cover page suppresses running header and footer. |
| 11 | **Pagination** | Dynamic Page Numbering | Footer contains dynamic `PAGE` and `NUMPAGES` fields. |
| 12 | **Appendix** | Source Code Completeness | All configured source files are present in the appendix. |
| 13 | **Visual QA** | Total Document Page Count | Minimum expected page threshold met (`min_expected_pages`). |
| 14 | **Visual QA** | Blank Page Detection | Pixel inspection detects accidental blank content pages (>98% white pixels). |

---

## Adding or Customizing an Assignment

To configure a new assignment or adjust existing scenarios, edit `tools/lab-report-generator/config.py`:

```python
ASSIGNMENT_REGISTRY[8] = AssignmentConfig(
    assignment_id=8,
    folder_name="Assignment-8",
    title="Lab Assignment 8: Full Stack Microservices",
    subtitle="REST API and Dynamic Client Integration",
    aim="To develop and evaluate...",
    server_type="express",  # 'static_http', 'express', or 'none'
    server_dir="Assignment-8",
    server_command=["node", "server.js"],
    default_port=3000,
    entry_url="/",
    software_requirements=[...],
    faculty_requirements=[...],
    procedure_steps=[...],
    source_files=[
        SourceFileSpec(
            relative_path="server.js",
            language="javascript",
            description="Express backend application server",
            role="Backend Server"
        ),
    ],
    scenes=[
        ScreenshotScene(
            name="01_dashboard_view",
            title="Application Dashboard",
            caption="Microservices Dashboard — Real-Time Health & Telemetry",
            description="Demonstrates dashboard interface loaded via HTTP GET on port 3000.",
            requirement_tag="Requirement 1: Dashboard UI",
            url_path="/"
        ),
    ],
    cli_commands=[
        CliCommandSpec(
            name="02_test_suite_execution",
            title="Automated Test Suite Execution",
            caption="Unit & Integration Tests — Jest Execution",
            description="Executes test runner verifying 100% test pass rate.",
            requirement_tag="Requirement 2: Automated Verification",
            command=["npm", "test"]
        ),
    ],
    viva_questions=[...],
    conclusion="...",
    min_expected_pages=10
)
```

---

## Troubleshooting Guide

### 1. Microsoft Word COM Conversion (`render_docx.py`)
- **Requirement:** Microsoft Word 2016, 2019, 2021, or Microsoft 365 must be installed on Windows.
- **Symptom:** `Microsoft Word PDF conversion failed: ...`
- **Solution:** Ensure Word is installed and activated. Close background dialogs using:
  ```powershell
  Stop-Process -Name WINWORD -Force -ErrorAction SilentlyContinue
  ```
- **Fallback:** If Word is not installed, use `-SkipRender` to generate the `.docx` document and screenshots without failing.

### 2. MongoDB Dependency (Assignments 6 & 7)
- **Requirement:** MongoDB Community Server (v6+) must be running locally on `mongodb://127.0.0.1:27017/`.
- **Symptom:** `MongooseServerSelectionError: connect ECONNREFUSED 127.0.0.1:27017`
- **Solution:** Start the local MongoDB service:
  ```powershell
  Start-Service -Name MongoDB
  # Or start mongod manually
  & "C:\Program Files\MongoDB\Server\7.0\bin\mongod.exe" --dbpath C:\data\db
  ```

### 3. Port Occupied / Server Conflicts
- **Symptom:** `Port 3000 is occupied by an external process.`
- **Solution:** The generator automatically detects occupied ports and chooses the next free port. You can also specify `-Port 3050` manually.

### 4. Missing Python Dependencies
- **Symptom:** `ModuleNotFoundError: No module named 'pypdfium2'` or `'playwright'`
- **Solution:** Activate the local virtual environment and install dependencies:
  ```powershell
  .\tools\lab-report-generator\.venv\Scripts\Activate.ps1
  pip install -r tools\lab-report-generator\requirements.txt
  playwright install chromium
  ```
