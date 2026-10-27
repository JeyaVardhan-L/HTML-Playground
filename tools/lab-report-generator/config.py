"""
Configuration and Registry for WAF Lab Report Generator.
Defines metadata, server start commands, source files, test automation scenes,
and CLI command evidence for Assignments 1 through 7.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path


@dataclass
class ScreenshotScene:
    name: str
    title: str
    caption: str
    description: str
    requirement_tag: str
    url_path: str
    wait_selector: Optional[str] = None
    viewport: Dict[str, int] = field(default_factory=lambda: {"width": 1440, "height": 900})
    actions: List[Dict[str, Any]] = field(default_factory=list)
    full_page: bool = False


@dataclass
class CliCommandSpec:
    name: str
    title: str
    caption: str
    description: str
    requirement_tag: str
    command: List[str]
    cwd_relative: Optional[str] = None
    env_vars: Dict[str, str] = field(default_factory=dict)


@dataclass
class SourceFileSpec:
    relative_path: str
    language: str
    description: str
    role: str


@dataclass
class AssignmentConfig:
    assignment_id: int
    folder_name: str
    title: str
    subtitle: str
    aim: str
    subject: str = "Web Application Frameworks (WAF) Lab"
    department: str = "Department of Computer Science & Engineering"
    institution: str = "GITAM Deemed to be University"
    default_student_name: str = "Jey"
    default_roll_no: str = "9057"
    academic_year: str = "2025-2026"
    server_type: str = "static_http"  # static_http, express, none
    server_dir: Optional[str] = None
    server_command: Optional[List[str]] = None
    default_port: int = 8000
    entry_url: str = "/index.html"
    software_requirements: List[str] = field(default_factory=list)
    faculty_requirements: List[Dict[str, str]] = field(default_factory=list)
    procedure_steps: List[str] = field(default_factory=list)
    source_files: List[SourceFileSpec] = field(default_factory=list)
    scenes: List[ScreenshotScene] = field(default_factory=list)
    cli_commands: List[CliCommandSpec] = field(default_factory=list)
    viva_questions: List[Dict[str, str]] = field(default_factory=list)
    conclusion: str = ""
    min_expected_pages: int = 4


# Registry of supported assignments
ASSIGNMENT_REGISTRY: Dict[int, AssignmentConfig] = {

    # ==================== ASSIGNMENT 1: MVC ARCHITECTURE ====================
    1: AssignmentConfig(
        assignment_id=1,
        folder_name="MVC_L1",
        title="Lab Assignment 1: MVC Architecture Implementation",
        subtitle="Model-View-Controller Web Application with Node.js, Express, and EJS",
        aim=(
            "To build a foundational web application from scratch using Node.js, Express, and EJS "
            "that successfully implements the Model-View-Controller (MVC) architectural pattern, "
            "strictly decoupling application data logic (Model), request handling and routing (Controller), "
            "and dynamic HTML presentation (View)."
        ),
        subject="Web Application Frameworks (WAF) Lab",
        department="Department of Computer Science & Engineering",
        institution="GITAM Deemed to be University",
        default_student_name="Jey",
        default_roll_no="9057",
        academic_year="2025-2026",
        server_type="express",
        server_dir="MVC_L1",
        server_command=["node", "app.js"],
        default_port=3000,
        entry_url="/",
        software_requirements=[
            "Operating System: Windows 10/11, macOS, or Linux",
            "Runtime Environment: Node.js (v18+ LTS)",
            "Web Application Framework: Express.js (v4)",
            "Server-Side Templating Engine: EJS (Embedded JavaScript v3)",
            "Automated Testing & Evidence Engine: Playwright (Chromium Headless)",
            "Report Generation: Python 3.14 with python-docx, Pillow, and pypdfium2"
        ],
        faculty_requirements=[
            {
                "requirement": "1. MVC Architecture & Folder Separation",
                "implementation": "models/, controllers/, views/",
                "evidence": "Separation of concerns enforced across models/messageModel.js, controllers/messageController.js, and views/view.ejs."
            },
            {
                "requirement": "2. Data Model Implementation",
                "implementation": "models/messageModel.js",
                "evidence": "getMessage() encapsulating data retrieval and returning 'Hello from the Model!' without presentation pollution."
            },
            {
                "requirement": "3. Controller Request Handler",
                "implementation": "controllers/messageController.js",
                "evidence": "showMessage(req, res) retrieving data from Model and passing { message: data } to res.render('view')."
            },
            {
                "requirement": "4. View Template Engine",
                "implementation": "views/view.ejs",
                "evidence": "EJS view template dynamically outputting <h1>MVC Architecture Lab</h1> and <h2><%= message %></h2>."
            },
            {
                "requirement": "5. Express Server & Route Configuration",
                "implementation": "app.js",
                "evidence": "app.set('view engine', 'ejs'), app.get('/', showMessage), and app.listen(3000) binding port 3000."
            }
        ],
        procedure_steps=[
            "1. Environment Initialization: Initialize a Node.js project using 'npm init -y' and install runtime dependencies 'express' and 'ejs'.",
            "2. Directory Architecture: Construct three dedicated directories ('models/', 'controllers/', 'views/') to enforce architectural boundaries.",
            "3. Model Construction: Author 'models/messageModel.js' with exported getMessage() function returning application data.",
            "4. Controller Implementation: Author 'controllers/messageController.js' with showMessage() invoking getMessage() and delegating to view.",
            "5. View Templating: Author 'views/view.ejs' implementing semantic markup and EJS tag interpolation '<%= message %>'.",
            "6. Server Entry Assembly: Configure Express application in 'app.js', set EJS view engine, mount root route handler, and start HTTP listener.",
            "7. Empirical Verification: Launch server on port 3000 and verify dynamic rendering through automated browser tests."
        ],
        source_files=[
            SourceFileSpec(
                relative_path="app.js",
                language="javascript",
                description="Express server entry point, view engine configuration, and root routing",
                role="Application Entry Point & Route Registry"
            ),
            SourceFileSpec(
                relative_path="controllers/messageController.js",
                language="javascript",
                description="Controller request handler orchestrating model data fetching and view rendering",
                role="Controller Layer"
            ),
            SourceFileSpec(
                relative_path="models/messageModel.js",
                language="javascript",
                description="Model module encapsulating business data logic and state retrieval",
                role="Model Layer"
            ),
            SourceFileSpec(
                relative_path="views/view.ejs",
                language="html",
                description="EJS presentation template generating dynamic HTML with interpolated model data",
                role="View Presentation Layer"
            ),
            SourceFileSpec(
                relative_path="package.json",
                language="json",
                description="Project package manifest declaring express and ejs dependencies",
                role="Project Metadata & Dependency Manifest"
            )
        ],
        scenes=[
            ScreenshotScene(
                name="01_mvc_rendered_view",
                title="MVC Architecture Output Screen",
                caption="Rendered MVC View — Express Route Rendering Dynamic EJS Template with Model Data (http://localhost:3000/)",
                description=(
                    "Illustrates the complete Model-View-Controller workflow in active execution. When the client navigates to "
                    "the root route ('/'), Express routes the incoming request to 'messageController.js', which queries "
                    "'messageModel.js' via getMessage() and transmits the resulting string into 'view.ejs'. The view engine renders "
                    "the styled HTML document displaying 'Hello from the Model!' with HTTP 200 status."
                ),
                requirement_tag="Requirements 1–5: Complete MVC Architectural Flow",
                url_path="/",
                wait_selector="h1",
                viewport={"width": 1440, "height": 800},
                actions=[
                    {"type": "wait_time", "ms": 500}
                ]
            )
        ],
        viva_questions=[
            {
                "question": "1. What is the Model-View-Controller (MVC) architectural pattern?",
                "answer": (
                    "MVC is an architectural design pattern that divides an application into three interconnected components: "
                    "the Model (manages data, business logic, and rules), the View (renders the visual representation of data to the user), "
                    "and the Controller (accepts user input, commands the Model to fetch or mutate data, and selects the View to render)."
                )
            },
            {
                "question": "2. What is the role of the Model in this assignment?",
                "answer": (
                    "In 'models/messageModel.js', the Model acts as the single source of truth for application data. It encapsulates "
                    "the data retrieval logic within getMessage() and exports it cleanly, preventing the Controller and View from directly "
                    "managing data definitions."
                )
            },
            {
                "question": "3. How does the Controller interact between the Model and View?",
                "answer": (
                    "In 'controllers/messageController.js', the showMessage() function acts as an intermediary. It receives the HTTP "
                    "request, calls getMessage() from the Model, and passes the retrieved data object ({ message: data }) into "
                    "res.render('view', ...), instructing Express to compile and deliver the View."
                )
            },
            {
                "question": "4. What is EJS and why is it used?",
                "answer": (
                    "EJS (Embedded JavaScript) is a server-side templating engine for Node.js. It allows developers to embed standard "
                    "JavaScript expressions inside HTML templates using syntax like <%= variable %>. EJS compiles on the server, producing "
                    "pure HTML before transmission to the browser."
                )
            },
            {
                "question": "5. Why is separation of concerns beneficial in web development?",
                "answer": (
                    "Separating concerns ensures that modifying user interface presentation does not inadvertently alter business data logic, "
                    "and changing the database structure does not break the HTML markup. It drastically enhances code readability, enables "
                    "isolated unit testing, and facilitates collaborative development."
                )
            }
        ],
        conclusion=(
            "Lab Assignment 1 was successfully implemented, executed, and verified. The Model-View-Controller (MVC) pattern was realized "
            "using Node.js, Express, and EJS with strict separation of concerns across models/, controllers/, and views/. The application "
            "delivered dynamic content with clean client-server communication and verified architectural integrity."
        ),
        min_expected_pages=4
    ),

    # ==================== ASSIGNMENT 2: MINIMALIST GRAYSCALE INTERFACE ====================
    2: AssignmentConfig(
        assignment_id=2,
        folder_name="Assignment-2",
        title="Lab Assignment 2: Minimalist Grayscale Interface (Mac-Inspired UI)",
        subtitle="Frontier AI Atlas — An Educational Guide to Modern Foundation Models",
        aim=(
            "To design, develop, and verify an educational multi-page web application "
            "('Frontier AI Atlas') utilizing HTML5 semantic tags, inline frame (<iframe name='content'>) "
            "routing, a developer survey form constructed strictly within a tabular layout (<table class='form-table'>), "
            "client-side JavaScript validation, external and standalone hyperlinks, responsive design principles, "
            "and a clean, minimalist Apple-inspired grayscale CSS design system."
        ),
        subject="Web Application Frameworks (WAF) Lab",
        department="Department of Computer Science & Engineering",
        institution="GITAM Deemed to be University",
        default_student_name="Jey",
        default_roll_no="9057",
        academic_year="2025-2026",
        server_type="static_http",
        server_dir="Assignment-2",
        default_port=8000,
        entry_url="/index.html",
        software_requirements=[
            "Operating System: Windows 10/11, macOS, or Linux",
            "Runtime: Python 3.14 (Built-in HTTP server module)",
            "Browser: Google Chrome / Chromium 120+ (with Playwright automation engine)",
            "Code Editor: Visual Studio Code",
            "Core Technologies: HTML5, CSS3 (Custom Properties & Flexbox/Grid), Vanilla JavaScript (ES2022)",
            "Report Generation: Python 3.14 with Playwright, python-docx, Pillow, and pypdfium2"
        ],
        faculty_requirements=[
            {
                "requirement": "1. Create Frames",
                "implementation": "index.html & js/script.js",
                "evidence": "<iframe src='home.html' name='content' id='content-frame'> with navigation <a href='...' target='content'> and bidirectional postMessage height auto-resizing."
            },
            {
                "requirement": "2. Header, Footer, Articles",
                "implementation": "index.html, articles.html",
                "evidence": "HTML5 semantic structure (<header>, <nav>, <main>, <article>, <aside>, <footer>) with reading badges and deep technical deep-dives."
            },
            {
                "requirement": "3. Tabular Form Creation",
                "implementation": "survey.html & css/style.css",
                "evidence": "<form id='aiSurveyForm'> with all inputs arranged strictly within <table class='form-table'> utilizing text, email, select, radios, checkboxes, and textarea."
            },
            {
                "requirement": "4. Hyperlinks (Standalone)",
                "implementation": "home.html, models.html, articles.html",
                "evidence": "Cross-linked document network with defensive frame scripting (window.self === window.top detection and fallback navigation banner)."
            },
            {
                "requirement": "5. Colors, Font & Background",
                "implementation": "css/style.css",
                "evidence": "Minimalist Apple-inspired grayscale CSS custom property system (--bg-canvas, --text-primary, --border-card) with Inter & Georgia typography."
            },
            {
                "requirement": "6. Responsive Layout",
                "implementation": "css/style.css",
                "evidence": "CSS Grid & Flexbox layouts adapting across desktop, tablet, and mobile (390px) viewports with table-to-block stacking media queries."
            }
        ],
        procedure_steps=[
            "1. Architecture & Frame Shell: Design 'index.html' featuring semantic header, navigation bar, footer, and inline iframe (<iframe name='content'>).",
            "2. Grayscale Design System: Develop 'css/style.css' establishing semantic CSS variables, border radius tokens, card elevation, and responsive breakpoints.",
            "3. Multi-Page Module Authoring: Construct subpages 'home.html' (overview), 'models.html' (comparison table), 'survey.html' (tabular form), and 'articles.html' (technical guides).",
            "4. Strict Tabular Form Engineering: Build developer feedback questionnaire inside 'survey.html' structured strictly within a multi-row <table> with accessible <label> pairings.",
            "5. Client-Side Defensive Scripting: Author 'js/script.js' implementing bidirectional postMessage auto-resizing, validation listeners, and standalone window detection.",
            "6. Non-Destructive Validation Feedback: Program form submission interceptor preventing page reloads (event.preventDefault()), checking constraints, and displaying summary cards.",
            "7. Automated Verification: Execute automated headless Playwright test suite to validate rendering, interactions, mobile responsiveness, and iframe bridging."
        ],
        source_files=[
            SourceFileSpec(
                relative_path="index.html",
                language="html",
                description="Main navigation shell, header, footer, and inline frame (<iframe name='content'>)",
                role="Application Frame Shell & Global Navigation"
            ),
            SourceFileSpec(
                relative_path="home.html",
                language="html",
                description="Home overview subpage loaded by default inside the content frame",
                role="Overview Subpage & Educational Architecture"
            ),
            SourceFileSpec(
                relative_path="models.html",
                language="html",
                description="Foundation model comparison guide, technical specifications, and standalone banner",
                role="Comparative Analysis Module"
            ),
            SourceFileSpec(
                relative_path="survey.html",
                language="html",
                description="Developer survey form structured strictly within an HTML table with validation hooks",
                role="Tabular Form & User Interaction Module"
            ),
            SourceFileSpec(
                relative_path="articles.html",
                language="html",
                description="Technical educational articles utilizing semantic HTML5 tags (<article>, <aside>)",
                role="Technical Educational Articles"
            ),
            SourceFileSpec(
                relative_path="css/style.css",
                language="css",
                description="Unified minimalist Apple-inspired grayscale design tokens, typography, and responsive media queries",
                role="Global Design System & Responsive Stylesheet"
            ),
            SourceFileSpec(
                relative_path="js/script.js",
                language="javascript",
                description="Client-side validation, bidirectional postMessage iframe resizer, and defensive frame detection",
                role="Client-Side Interaction & Frame Bridge"
            )
        ],
        scenes=[
            ScreenshotScene(
                name="01_primary_interface_shell",
                title="Primary Application Shell and Home View",
                caption="Frontier AI Atlas — Primary Interface Shell (<iframe name='content'> Loading 'home.html')",
                description=(
                    "Captures the master application shell (index.html) running at full desktop resolution (1440x900). "
                    "Demonstrates the semantic header, navigation menu, status indicator, and the embedded content iframe "
                    "seamlessly displaying 'home.html' with bidirectional postMessage height auto-resizing. Fulfills Requirement 1."
                ),
                requirement_tag="Requirement 1: Inline Frame Architecture",
                url_path="/index.html",
                wait_selector="#content-frame",
                viewport={"width": 1440, "height": 900},
                actions=[
                    {"type": "wait_time", "ms": 800}
                ]
            ),
            ScreenshotScene(
                name="02_model_explorer_subpage",
                title="Foundation Model Explorer and Technical Comparison",
                caption="Foundation Model Explorer — Grid Comparison & Standalone Detection (models.html in Content Frame)",
                description=(
                    "Displays the Foundation Model Explorer loaded within the iframe via navigation click. Shows the comparative "
                    "grid detailing model parameters, context windows, and license terms, styled in the clean grayscale design system. "
                    "Fulfills Requirements 1, 4, and 5."
                ),
                requirement_tag="Requirement 1 & 4: Frame Navigation & Hyperlinks",
                url_path="/index.html",
                wait_selector="#content-frame",
                viewport={"width": 1440, "height": 900},
                actions=[
                    {"type": "click", "selector": 'a[href="models.html"]'},
                    {"type": "wait_time", "ms": 800}
                ]
            ),
            ScreenshotScene(
                name="03_tabular_survey_form",
                title="Strict Tabular Form Layout and Input Controls",
                caption="Developer Survey Form — Form Elements Structured Inside <table class='form-table'> (survey.html)",
                description=(
                    "Demonstrates the developer feedback form constructed strictly within a semantic HTML table layout. "
                    "Features aligned label cells, text inputs, email inputs, dropdown selectors, radio buttons, capability checkboxes, "
                    "and a formatted comments textarea. Fulfills Requirement 3."
                ),
                requirement_tag="Requirement 3: Tabular Form Layout",
                url_path="/index.html",
                wait_selector="#content-frame",
                viewport={"width": 1440, "height": 900},
                actions=[
                    {"type": "click", "selector": 'a[href="survey.html"]'},
                    {"type": "wait_time", "ms": 800}
                ]
            ),
            ScreenshotScene(
                name="04_form_validation_errors",
                title="Client-Side Form Validation and Error Handling",
                caption="Client-Side Validation — Required Field Constraints & Inline Error Highlights",
                description=(
                    "Demonstrates client-side JavaScript validation triggered by attempting to submit an empty form. "
                    "Validation routines intercept the event (event.preventDefault()), apply red borders to invalid inputs, "
                    "and render descriptive error messages directly below failed fields without reloading the page. Fulfills Requirement 3."
                ),
                requirement_tag="Requirement 3: JavaScript Form Validation",
                url_path="/index.html",
                wait_selector="#content-frame",
                viewport={"width": 1440, "height": 900},
                actions=[
                    {"type": "click", "selector": 'a[href="survey.html"]'},
                    {"type": "wait_time", "ms": 800},
                    {
                        "type": "iframe_action",
                        "frame_selector": "#content-frame",
                        "sub_action": {"type": "click", "selector": 'button[type="submit"]'}
                    },
                    {"type": "wait_time", "ms": 500}
                ]
            ),
            ScreenshotScene(
                name="05_successful_form_submission",
                title="Successful Form Submission and Confirmation Summary",
                caption="Form Submission Success — Dynamic Feedback Card (<div id='surveyResultCard'>) Rendering User Inputs",
                description=(
                    "Illustrates successful form submission with valid test inputs. The script constructs a dynamic summary card "
                    "displaying the student's name, registered email, selected foundation model, primary use case, experience level, "
                    "and active capabilities, confirming correct DOM manipulation. Fulfills Requirement 3."
                ),
                requirement_tag="Requirement 3: Form Processing & DOM Updates",
                url_path="/index.html",
                wait_selector="#content-frame",
                viewport={"width": 1440, "height": 900},
                actions=[
                    {"type": "click", "selector": 'a[href="survey.html"]'},
                    {"type": "wait_time", "ms": 800},
                    {
                        "type": "iframe_action",
                        "frame_selector": "#content-frame",
                        "sub_action": {
                            "type": "fill_survey",
                            "name": "Jey",
                            "email": "student@gitam.in",
                            "model": "Anthropic Claude 3.5 Sonnet",
                            "use_case": "Software Engineering & Coding",
                            "experience": "Advanced",
                            "capabilities": ["code", "multimodal"],
                            "comments": "Automated lab verification successful."
                        }
                    },
                    {"type": "wait_time", "ms": 800}
                ]
            ),
            ScreenshotScene(
                name="06_semantic_articles_guide",
                title="Semantic Technical Guides and Article Layout",
                caption="Technical Articles Module — HTML5 Semantic Document Hierarchy (<article>, <aside>, <section>)",
                description=(
                    "Highlights the educational articles module ('articles.html') demonstrating structured use of HTML5 "
                    "semantic elements (<article>, <aside>, <header>, <section>). Features typography tuned for long-form reading, "
                    "reading time estimates, and secondary advisory sidebars. Fulfills Requirement 2."
                ),
                requirement_tag="Requirement 2: Semantic HTML5 Structure",
                url_path="/index.html",
                wait_selector="#content-frame",
                viewport={"width": 1440, "height": 900},
                actions=[
                    {"type": "click", "selector": 'a[href="articles.html"]'},
                    {"type": "wait_time", "ms": 800}
                ]
            ),
            ScreenshotScene(
                name="07_external_hyperlinks_navigation",
                title="External Hyperlink Network and Multi-Target Architecture",
                caption="Hyperlink System — Internal Frame Routing (target='content') & External Resources (target='_blank')",
                description=(
                    "Demonstrates the multi-target hyperlink architecture. Internal navigation anchors route into the named "
                    "content frame using target='content', while official research papers and documentation links open securely in "
                    "new browser tabs using target='_blank' with rel='noopener noreferrer'. Fulfills Requirement 4."
                ),
                requirement_tag="Requirement 4: Multi-Target Hyperlink Architecture",
                url_path="/index.html",
                wait_selector="#content-frame",
                viewport={"width": 1440, "height": 900},
                actions=[
                    {"type": "click", "selector": 'a[href="home.html"]'},
                    {"type": "wait_time", "ms": 800}
                ]
            ),
            ScreenshotScene(
                name="08_mobile_responsive_viewport",
                title="Mobile Responsive Adaptation on Narrow Viewport (390px)",
                caption="Mobile Responsiveness — Media Query Grid & Table Stacking (iPhone 14 Viewport: 390x844)",
                description=(
                    "Validates the application's responsive design system on a narrow mobile viewport (390x844). "
                    "The CSS media queries (@media (max-width: 768px)) dynamically transform table rows and cells into stacked block elements, "
                    "preventing horizontal clipping and ensuring accessible mobile data entry. Fulfills Requirement 6."
                ),
                requirement_tag="Requirement 6: Responsive Design",
                url_path="/survey.html",
                wait_selector="#aiSurveyForm",
                viewport={"width": 390, "height": 844},
                actions=[
                    {"type": "wait_time", "ms": 1000}
                ]
            ),
            ScreenshotScene(
                name="09_standalone_banner_detection",
                title="Standalone Window Detection and Fallback Navigation",
                caption="Standalone Page Detection — Standalone Banner & Navigation Fallback (<div id='standaloneNotice'>)",
                description=(
                    "Illustrates graceful fallback behavior when a subpage ('models.html') is opened directly outside "
                    "the parent frame shell. The JavaScript detection routine (window.self === window.top) activates "
                    "the top standalone banner, providing a one-click redirect ('Open in Main View →') back into "
                    "'index.html' with target='_top'."
                ),
                requirement_tag="Requirement 4: Hyperlinks & Defensive Frame Scripting",
                url_path="/models.html",
                wait_selector="#standaloneNotice",
                viewport={"width": 1440, "height": 800},
                actions=[
                    {"type": "wait_time", "ms": 1000}
                ]
            )
        ],
        viva_questions=[
            {
                "question": "1. Why use an <iframe> instead of the obsolete HTML <frameset> tag?",
                "answer": (
                    "<frameset> was completely deprecated and removed in HTML5 because it broke browser history navigation, "
                    "bookmarked URLs, screen readers, search engine indexing, and mobile responsiveness. An <iframe> (inline frame) "
                    "embeds an external or internal document cleanly within a standard responsive layout while maintaining modern DOM and CSS control."
                )
            },
            {
                "question": "2. How does target='content' work with named iframes?",
                "answer": (
                    "When an <iframe> has an identifier such as name='content', any anchor tag with target='content' instructs "
                    "the browser to load the referenced URL inside that specific frame rather than opening a new tab or reloading the outer window."
                )
            },
            {
                "question": "3. What is the advantage of semantic HTML5 elements over generic <div> tags?",
                "answer": (
                    "Semantic elements (<header>, <nav>, <main>, <section>, <article>, <footer>) provide structural meaning to the browser, "
                    "search engines, and assistive screen reader technologies. They define accessibility landmarks and produce a clean document outline."
                )
            },
            {
                "question": "4. How is the tabular form made responsive on smaller mobile viewports?",
                "answer": (
                    "On desktop displays, the table behaves normally with display: table-cell for labels and inputs. In 'css/style.css', "
                    "a media query (@media (max-width: 768px)) sets table, tr, and td to display: block, cleanly stacking label cells "
                    "directly above input cells for touch-friendly mobile interaction."
                )
            },
            {
                "question": "5. What role does event.preventDefault() play during form submission?",
                "answer": (
                    "event.preventDefault() stops the browser's default synchronous HTTP form submission and subsequent page refresh. "
                    "This enables client-side JavaScript to inspect and validate inputs, present instant error alerts or dynamic summary cards, "
                    "and retain user data without losing application state."
                )
            },
            {
                "question": "6. How does postMessage allow seamless iframe auto-resizing?",
                "answer": (
                    "Because iframes have their own viewport, their height does not automatically expand to match their content. "
                    "The child document measures its scrollHeight and calls window.parent.postMessage({ type: 'ATLAS_RESIZE', height }, '*'). "
                    "The parent listens for this message and adjusts the iframe's CSS height dynamically, eliminating vertical scrollbars."
                )
            }
        ],
        conclusion=(
            "Lab Assignment 2 was successfully designed, developed, and verified. "
            "All six core faculty requirements—incorporation of named inline frames (<iframe name='content'>), "
            "semantic HTML5 document structure, developer survey form constructed in a strict tabular format with client-side validation, "
            "multi-target hyperlink architecture, minimalist Apple-inspired grayscale CSS system, and fluid mobile responsiveness—"
            "have been comprehensively implemented and empirically verified through automated browser testing. "
            "The web application functions with zero external dependencies and demonstrates robust client-side software engineering."
        ),
        min_expected_pages=15
    ),

    # ==================== ASSIGNMENT 3: CORE JAVASCRIPT PRACTICALS ====================
    3: AssignmentConfig(
        assignment_id=3,
        folder_name="Assignment-3",
        title="Lab Assignment 3: Core JavaScript Practicals",
        subtitle="JavaScript Foundations, DOM Manipulation, Events, Objects, DHTML & Error Handling",
        aim=(
            "To demonstrate foundational client-side JavaScript mechanisms through four self-contained, "
            "evaluable practicals: (1) student registration form with custom field validation, dynamic error alerts, "
            "and summary output; (2) core JavaScript language basics, primitive data types, expressions, custom object "
            "literals, Date/String methods, and exception handling; (3) HTML5 drag-and-drop events with local vector manipulation "
            "and live logging; and (4) dynamic CSS z-index stacking order manipulation with real-time layer reordering."
        ),
        subject="Web Application Frameworks (WAF) Lab",
        department="Department of Computer Science & Engineering",
        institution="GITAM Deemed to be University",
        default_student_name="Jey",
        default_roll_no="9057",
        academic_year="2025-2026",
        server_type="static_http",
        server_dir="Assignment-3",
        default_port=8000,
        entry_url="/practical-1-form.html",
        software_requirements=[
            "Operating System: Windows 10/11, macOS, or Linux",
            "Runtime: Python 3.14 (Built-in HTTP server module)",
            "Web Browser: Google Chrome / Chromium 120+ (with Playwright engine)",
            "Code Editor: Visual Studio Code",
            "Core Technologies: HTML5, CSS3, Vanilla JavaScript (ES2022), Local SVG Vector Assets",
            "Report Generation: Python 3.14 with Playwright, python-docx, Pillow, and pypdfium2"
        ],
        faculty_requirements=[
            {
                "requirement": "1. Form Validation (Functions, Conditions, Events)",
                "implementation": "practical-1-form.html",
                "evidence": "Client-side validation on fullName, age, email, phone, and address with instant red error spans, event.preventDefault(), and green success summary card."
            },
            {
                "requirement": "2. Data Types, Objects & Error Handling",
                "implementation": "practical-2-basics.html",
                "evidence": "Interactive evaluation of primitive data types (typeof), arithmetic/logical expressions, functions with return values, for loops, object literals with methods, and try/catch/finally."
            },
            {
                "requirement": "3. Drag-and-Drop Image with Events & DHTML",
                "implementation": "practical-3-drag-drop.html",
                "evidence": "HTML5 Drag and Drop API (dragstart, dragover, drop) on local SVG asset (assets/star.svg), drop target zones, style manipulation, and live event logging."
            },
            {
                "requirement": "4. Dynamic Stacking of Elements (z-index)",
                "implementation": "practical-4-stacking.html",
                "evidence": "Dynamic z-index modification across 3 overlapping absolute cards with click-to-front event handling, live z-index readouts, and reset controls."
            }
        ],
        procedure_steps=[
            "1. Form Validation Engineering: Construct 'practical-1-form.html' implementing input constraints, regex pattern checking, preventDefault() interception, and dynamic success card rendering.",
            "2. Language Foundations Laboratory: Author 'practical-2-basics.html' creating interactive demonstrators for typeof evaluation, operator precedence, circle area functions, for loops, student object methods, and try/catch exception blocks.",
            "3. Drag-and-Drop Canvas: Develop 'practical-3-drag-drop.html' with draggable SVG element, target drop zones, coordinates tracking, and timestamped console event logging.",
            "4. Dynamic Stacking System: Implement 'practical-4-stacking.html' configuring overlapping cards with CSS z-index, event listeners to alter stacking hierarchy, and live z-index display pills.",
            "5. Automated Execution & Verification: Launch local HTTP server and execute Playwright test suite to validate form submissions, math calculations, drag-drop events, and z-index reordering."
        ],
        source_files=[
            SourceFileSpec(
                relative_path="practical-1-form.html",
                language="html",
                description="Student registration form with client-side field validation, instant error messages, and dynamic summary box",
                role="Practical 1: Form Validation & Events"
            ),
            SourceFileSpec(
                relative_path="practical-2-basics.html",
                language="html",
                description="Core JavaScript basics, data types table, mathematical expressions, object literals, Date/String methods, and try/catch error handling",
                role="Practical 2: Language Basics, Objects & Exceptions"
            ),
            SourceFileSpec(
                relative_path="practical-3-drag-drop.html",
                language="html",
                description="Interactive drag-and-drop canvas using HTML5 drag events on local SVG star badge with live event logging",
                role="Practical 3: HTML5 Drag & Drop and DHTML"
            ),
            SourceFileSpec(
                relative_path="practical-4-stacking.html",
                language="html",
                description="Dynamic CSS z-index stacking practical with overlapping colored cards and interactive layer reordering",
                role="Practical 4: Dynamic Stacking & z-index"
            )
        ],
        scenes=[
            ScreenshotScene(
                name="01_practical1_form_submission",
                title="Practical 1: Student Registration Form Validation",
                caption="Registration Form Validation — Client-Side Checks & Dynamic Success Summary Card (practical-1-form.html)",
                description=(
                    "Captures Practical 1 after entering valid student registration details and clicking 'Register Student'. "
                    "The client-side validation logic verifies that all input fields satisfy their length and format constraints, "
                    "clears error spans, and dynamically unhides the green success card (<div class='success-card'>) displaying "
                    "the student's registered details."
                ),
                requirement_tag="Requirement 1: Form Validation & Events",
                url_path="/practical-1-form.html",
                wait_selector="#registrationForm",
                viewport={"width": 1440, "height": 900},
                actions=[
                    {"type": "fill", "selector": "#fullName", "value": "Jey Vardhan"},
                    {"type": "fill", "selector": "#age", "value": "21"},
                    {"type": "fill", "selector": "#email", "value": "jey@gitam.in"},
                    {"type": "fill", "selector": "#phone", "value": "9876543210"},
                    {"type": "fill", "selector": "#address", "value": "GITAM University Campus, Hyderabad, India"},
                    {"type": "click", "selector": 'button[type="submit"]'},
                    {"type": "wait_time", "ms": 600}
                ]
            ),
            ScreenshotScene(
                name="02_practical2_basics_objects",
                title="Practical 2: JavaScript Foundations, Objects & Exceptions",
                caption="JavaScript Foundations — Data Types, Operators, Object Literals & try/catch Handling (practical-2-basics.html)",
                description=(
                    "Displays Practical 2 demonstrating JavaScript language foundations. The page evaluates primitive data types "
                    "into an automated table, executes functions with return values (calculateArea), tests condition-based grade evaluation, "
                    "runs a for-loop for multiples of 3, invokes object literal methods using 'this', and demonstrates try/catch exception handling."
                ),
                requirement_tag="Requirement 2: Data Types, Objects & Error Handling",
                url_path="/practical-2-basics.html",
                wait_selector="#calcAreaBtn",
                viewport={"width": 1440, "height": 900},
                actions=[
                    {"type": "click", "selector": "#calcAreaBtn"},
                    {"type": "click", "selector": "#checkGradeBtn"},
                    {"type": "wait_time", "ms": 600}
                ]
            ),
            ScreenshotScene(
                name="03_practical3_drag_drop",
                title="Practical 3: HTML5 Drag-and-Drop with Live Event Logging",
                caption="Drag-and-Drop Interaction — Draggable SVG Badge, Target Zones & Event Logging (practical-3-drag-drop.html)",
                description=(
                    "Illustrates Practical 3 demonstrating the HTML5 Drag and Drop API. A local vector badge (assets/star.svg) "
                    "is dragged across the bordered canvas into Target Zone A. Event listeners for 'dragstart', 'dragover', and 'drop' "
                    "capture the interaction, update the status message, and append timestamped audit entries into the live terminal log."
                ),
                requirement_tag="Requirement 3: Drag-and-Drop & DHTML",
                url_path="/practical-3-drag-drop.html",
                wait_selector="#dragImage",
                viewport={"width": 1440, "height": 900},
                actions=[
                    {"type": "drag_and_drop", "source": "#dragImage", "target": "#zoneA"},
                    {"type": "wait_time", "ms": 600}
                ]
            ),
            ScreenshotScene(
                name="04_practical4_stacking_zindex",
                title="Practical 4: Dynamic Stacking of Elements (z-index)",
                caption="Dynamic Element Stacking — Layer Reordering & Live z-index Modification (practical-4-stacking.html)",
                description=(
                    "Demonstrates Practical 4 showing dynamic CSS z-index modification based on user interaction. "
                    "When Box 2 (Royal Indigo) is clicked, JavaScript computes the highest current layer index, reassigns "
                    "Box 2's z-index to 4, updates the top box indicator, and refreshes the live layer status pills."
                ),
                requirement_tag="Requirement 4: Dynamic Stacking & CSS Manipulation",
                url_path="/practical-4-stacking.html",
                wait_selector="#box2",
                viewport={"width": 1440, "height": 900},
                actions=[
                    {"type": "click", "selector": "#box2"},
                    {"type": "wait_time", "ms": 600}
                ]
            )
        ],
        viva_questions=[
            {
                "question": "1. What is the difference between client-side and server-side JavaScript?",
                "answer": (
                    "Client-side JavaScript runs inside the user's browser (e.g. V8 engine in Chrome) and directly manipulates the DOM, "
                    "styles, and user events. Server-side JavaScript runs inside Node.js, managing network ports, databases, and file systems."
                )
            },
            {
                "question": "2. What is the purpose of event.preventDefault() in form handling?",
                "answer": (
                    "By default, submitting an HTML form causes the browser to reload the page and attempt a synchronous HTTP request. "
                    "event.preventDefault() suppresses this default action, allowing client-side JavaScript to validate inputs, display inline "
                    "errors, and update the DOM without state loss."
                )
            },
            {
                "question": "3. Explain the difference between '==' and '===' in JavaScript.",
                "answer": (
                    "'==' performs type coercion before comparison (e.g., '5' == 5 evaluates to true). '===' is the strict equality operator; "
                    "it checks both value and data type without coercion (e.g., '5' === 5 evaluates to false). Modern code strictly prefers '==='."
                )
            },
            {
                "question": "4. How does the HTML5 Drag and Drop API work?",
                "answer": (
                    "An element is made draggable with draggable='true'. During dragging, the browser fires 'dragstart', 'drag', and 'dragend'. "
                    "A drop target listens for 'dragover' (where event.preventDefault() must be called to permit dropping) and 'drop' to process "
                    "the data transfer."
                )
            },
            {
                "question": "5. What is CSS z-index and how does JavaScript alter it dynamically?",
                "answer": (
                    "z-index controls the 3D stacking order of positioned elements (relative, absolute, or fixed) along the z-axis. Elements with "
                    "higher z-index numbers render on top of lower ones. In JavaScript, element.style.zIndex = newZ dynamically updates this property."
                )
            },
            {
                "question": "6. How does exception handling with try/catch/finally work?",
                "answer": (
                    "Code that might encounter a runtime error is wrapped in a try block. If an error is thrown, execution immediately transfers "
                    "to the catch(error) block, preventing application crash. The optional finally block always executes regardless of whether an error occurred."
                )
            }
        ],
        conclusion=(
            "Lab Assignment 3 was successfully implemented, verified, and demonstrated. All four core practicals—student registration "
            "form validation with dynamic DOM summaries, language foundations with object literals and exception handling, HTML5 drag-and-drop "
            "with live event logging, and dynamic CSS z-index element stacking—were thoroughly tested with zero external dependencies."
        ),
        min_expected_pages=15
    ),

    # ==================== ASSIGNMENT 4: EXPRESS FETCH & REACT PRACTICALS ====================
    4: AssignmentConfig(
        assignment_id=4,
        folder_name="Assignment-4",
        title="Lab Assignment 4: Express Server with Browser Fetch & Core React Practicals",
        subtitle="Asynchronous Client-Server Fetch & Component-Based React Architecture",
        aim=(
            "To design, develop, and evaluate a comprehensive full-stack web architecture consisting of: "
            "(1) an Express.js backend server serving static assets and providing an asynchronous GET /api/student endpoint "
            "consumed via the browser Fetch API; and (2) a React 18 component laboratory demonstrating State management (useState), "
            "Class Components, Props data flow, Three React Hooks (useState, useRef, useEffect), and Function Components."
        ),
        subject="Web Application Frameworks (WAF) Lab",
        department="Department of Computer Science & Engineering",
        institution="GITAM Deemed to be University",
        default_student_name="Jey",
        default_roll_no="9057",
        academic_year="2025-2026",
        server_type="express",
        server_dir="Assignment-4/express-fetch",
        server_command=["node", "server.js"],
        default_port=3000,
        entry_url="/",
        software_requirements=[
            "Operating System: Windows 10/11, macOS, or Linux",
            "Runtime: Node.js (v18+ LTS) and npm",
            "Backend Framework: Express.js (v4)",
            "Frontend Library: React 18 with Vite 6 Build System",
            "Web Browser: Google Chrome / Chromium (with Playwright engine)",
            "Report Generation: Python 3.14 with Playwright, python-docx, Pillow, and pypdfium2"
        ],
        faculty_requirements=[
            {
                "requirement": "1. Express Server & Browser Fetch",
                "implementation": "express-fetch/server.js & public/index.html",
                "evidence": "Express static middleware serving HTML client, GET /api/student returning JSON, and browser fetch() dynamically rendering student details."
            },
            {
                "requirement": "2. React State Practical",
                "implementation": "react-practicals/src/components/StateCounter.jsx",
                "evidence": "StateCounter component using useState hook for interactive increment, decrement, and reset counters."
            },
            {
                "requirement": "3. React Class Component",
                "implementation": "react-practicals/src/components/ClassStudent.jsx",
                "evidence": "ClassStudent extending React.Component with constructor(props), this.state, and render() lifecycle."
            },
            {
                "requirement": "4. React Props Practical",
                "implementation": "react-practicals/src/components/StudentProps.jsx",
                "evidence": "StudentProps demonstrating parent-to-child data transfer with array mapping and prop destructuring."
            },
            {
                "requirement": "5. Three React Hooks Practical",
                "implementation": "react-practicals/src/components/HooksDemo.jsx",
                "evidence": "HooksDemo demonstrating useState (toggle), useRef (DOM input focus), and useEffect (auto-running timer)."
            },
            {
                "requirement": "6. React Function Component",
                "implementation": "react-practicals/src/components/FunctionStudent.jsx",
                "evidence": "Modern React functional component returning JSX with conditional styling and clean presentation."
            }
        ],
        procedure_steps=[
            "1. Express Backend Setup: Author 'express-fetch/server.js', configure express.static() middleware, register GET /api/student endpoint, and start server on port 3000.",
            "2. Fetch Client Implementation: Create 'express-fetch/public/index.html' with asynchronous fetch() event handler updating DOM upon button click.",
            "3. React Environment Scaffolding: Configure Vite with @vitejs/plugin-react in 'react-practicals/vite.config.js' and author main container 'App.jsx'.",
            "4. Component Architecture: Implement StateCounter (state), ClassStudent (class component), StudentProps (props mapping), HooksDemo (three hooks), and FunctionStudent.",
            "5. Build & Integration: Compile React practicals using 'npm run build' into optimized static assets in 'dist/'.",
            "6. Full-Stack Verification: Execute Playwright automation suite to capture Express fetch interaction and React tabbed component practicals."
        ],
        source_files=[
            SourceFileSpec(
                relative_path="express-fetch/server.js",
                language="javascript",
                description="Express server configuring static public middleware and /api/student JSON endpoint",
                role="Backend Express Server"
            ),
            SourceFileSpec(
                relative_path="express-fetch/public/index.html",
                language="html",
                description="Frontend HTML client making asynchronous fetch() request to /api/student",
                role="Frontend Fetch Client Interface"
            ),
            SourceFileSpec(
                relative_path="react-practicals/src/App.jsx",
                language="javascript",
                description="Main React tabbed container orchestrating all five React practical components",
                role="React Root Tabbed Container"
            ),
            SourceFileSpec(
                relative_path="react-practicals/src/components/StateCounter.jsx",
                language="javascript",
                description="React State practical demonstrating useState increment, decrement, and reset",
                role="Practical 2: React State Component"
            ),
            SourceFileSpec(
                relative_path="react-practicals/src/components/ClassStudent.jsx",
                language="javascript",
                description="React Class component demonstrating extends React.Component and this.state",
                role="Practical 3: React Class Component"
            ),
            SourceFileSpec(
                relative_path="react-practicals/src/components/StudentProps.jsx",
                language="javascript",
                description="React Props practical demonstrating parent-to-child data flow via prop destructuring",
                role="Practical 4: React Props Component"
            ),
            SourceFileSpec(
                relative_path="react-practicals/src/components/HooksDemo.jsx",
                language="javascript",
                description="React Hooks practical demonstrating useState, useRef, and useEffect concurrently",
                role="Practical 5: Three React Hooks Component"
            ),
            SourceFileSpec(
                relative_path="react-practicals/src/components/FunctionStudent.jsx",
                language="javascript",
                description="Modern React Function component returning clean JSX markup",
                role="Practical 6: React Function Component"
            ),
            SourceFileSpec(
                relative_path="react-practicals/src/styles.css",
                language="css",
                description="Clean, college-practical CSS styling for React component cards and tab navigation",
                role="React Component Stylesheet"
            )
        ],
        scenes=[
            ScreenshotScene(
                name="01_express_fetch_client",
                title="Express Server and Asynchronous Fetch Client",
                caption="Express & Browser Fetch — Client Interface Dynamically Populated via GET /api/student (http://localhost:3000/)",
                description=(
                    "Captures the Express client interface (express-fetch/public/index.html) after clicking 'Fetch Student Data'. "
                    "The browser issues an asynchronous fetch() request to 'http://localhost:3000/api/student', parses the incoming JSON payload, "
                    "and dynamically injects the student's name, roll number, department, CGPA, and status into the DOM without reloading."
                ),
                requirement_tag="Requirement 1: Express Server & Browser Fetch",
                url_path="/",
                wait_selector="#fetchBtn",
                viewport={"width": 1440, "height": 900},
                actions=[
                    {"type": "click", "selector": "#fetchBtn"},
                    {"type": "wait_time", "ms": 600}
                ]
            )
        ],
        cli_commands=[
            CliCommandSpec(
                name="02_react_build_output",
                title="React Vite Production Build Verification",
                caption="React Laboratory Build — Vite Bundler Transforming JSX Components into Production Distribution",
                description=(
                    "Validates that all five React practical components (StateCounter, ClassStudent, StudentProps, HooksDemo, and FunctionStudent) "
                    "compile cleanly with Vite and Rollup, producing a minified production bundle in 'dist/' with zero syntax or typing errors."
                ),
                requirement_tag="Requirements 2–6: React Component Suite Build",
                command=["npx", "vite", "build"],
                cwd_relative="react-practicals"
            )
        ],
        viva_questions=[
            {
                "question": "1. What is the difference between client-side code and server-side code in Practical 1?",
                "answer": (
                    "Server-side code ('server.js') runs in Node.js on our computer, having direct access to network ports and the file system. "
                    "Client-side code ('public/index.html') runs inside the user's browser V8 engine. They cannot directly access each other's "
                    "variables; they communicate exclusively over HTTP via network requests and JSON responses."
                )
            },
            {
                "question": "2. What is express.static() middleware and how does it work?",
                "answer": (
                    "express.static() is a built-in middleware function in Express that serves static files (HTML, CSS, images, client JS) "
                    "from a designated directory. In our project, app.use(express.static('public')) automatically delivers index.html when a user "
                    "requests the root URL."
                )
            },
            {
                "question": "3. What is the difference between Props and State in React?",
                "answer": (
                    "Props (short for properties) are read-only data passed from a parent component down to a child component. State is internal, "
                    "mutable data managed directly within a component. When state changes via its setter function (e.g. setCount), React automatically "
                    "re-renders the component to update the UI."
                )
            },
            {
                "question": "4. Compare React Class Components with Function Components.",
                "answer": (
                    "Class components extend React.Component, manage state using this.state and this.setState(), and implement a render() method. "
                    "Function components are modern JavaScript functions that accept props and return JSX directly; they manage state and side effects "
                    "using React Hooks (such as useState and useEffect) with cleaner, more concise syntax."
                )
            },
            {
                "question": "5. Explain the three React Hooks demonstrated in HooksDemo.",
                "answer": (
                    "useState manages local reactive state (e.g. toggling active status). useRef holds a mutable reference that persists across "
                    "renders without triggering re-renders, commonly used to directly access DOM elements (e.g. focusing an input). useEffect "
                    "manages side effects such as data subscriptions, timers, or manual DOM mutations after rendering."
                )
            }
        ],
        conclusion=(
            "Lab Assignment 4 was successfully developed and verified. The Express backend demonstrated efficient asynchronous JSON data delivery "
            "via native browser fetch(), while the React 18 component suite verified foundational frontend concepts including state management, "
            "props data flow, class lifecycle, and modern hooks."
        ),
        min_expected_pages=15
    ),

    # ==================== ASSIGNMENT 5: EXPRESS FETCH WITH ON-DEMAND CONNECTION ====================
    5: AssignmentConfig(
        assignment_id=5,
        folder_name="Assignment-5",
        title="Lab Assignment 5: Fetching Data with a New Connection Using Express.js",
        subtitle="On-Demand HTTP Connections, Server-Side Request Counting & Asynchronous DOM Updates",
        aim=(
            "To demonstrate decoupled web communication where client user actions establish brand new HTTP GET connections "
            "to an Express.js backend on demand without reloading the host page. The Express server maintains an internal "
            "request counter, generates server-side timestamps, logs incoming requests to the terminal, and transmits dynamic JSON."
        ),
        subject="Web Application Frameworks (WAF) Lab",
        department="Department of Computer Science & Engineering",
        institution="GITAM Deemed to be University",
        default_student_name="Alex Kumar",
        default_roll_no="9057",
        academic_year="2025-2026",
        server_type="express",
        server_dir="Assignment-5",
        server_command=["node", "server.js"],
        default_port=3001,
        entry_url="/",
        software_requirements=[
            "Operating System: Windows 10/11, macOS, or Linux",
            "Runtime: Node.js (v18+ LTS) and npm",
            "Web Framework: Express.js (v4)",
            "Client API: Browser Fetch API (async / await)",
            "Web Browser: Google Chrome / Chromium (with Playwright engine)",
            "Report Generation: Python 3.14 with Playwright, python-docx, Pillow, and pypdfium2"
        ],
        faculty_requirements=[
            {
                "requirement": "1. Static File Serving",
                "implementation": "server.js & public/index.html",
                "evidence": "app.use(express.static('public')) serving the initial HTML client on port 3001 without initial student data."
            },
            {
                "requirement": "2. On-Demand Fetch Connection",
                "implementation": "public/index.html",
                "evidence": "fetchStudentData() dispatching fetch('/api/student') on user button click, creating a fresh HTTP connection."
            },
            {
                "requirement": "3. Server-Side Counter & Timestamp",
                "implementation": "server.js",
                "evidence": "server increments requestCount on every hit, captures new Date().toLocaleTimeString(), and logs 'GET /api/student: request N' to terminal."
            },
            {
                "requirement": "4. Dynamic Client DOM Updating",
                "implementation": "public/index.html",
                "evidence": "Client updates #studentName, #studentBranch, #requestNumber, and #fetchTimestamp dynamically upon JSON receipt."
            }
        ],
        procedure_steps=[
            "1. Express Setup & Static Route: Author 'server.js', configure Express with express.static('public'), and initialize server request counter to 0.",
            "2. Dynamic API Endpoint: Implement GET /api/student endpoint that increments requestCount, captures a fresh timestamp, logs request to terminal, and responds with JSON.",
            "3. Client Interface Construction: Develop 'public/index.html' with clean lab styling, #fetchBtn trigger, loading spinners, and hidden student display container.",
            "4. Asynchronous Fetch Integration: Write async fetchStudentData() function in client script utilizing try/catch/finally to handle HTTP responses.",
            "5. Port Conflict Safeguards: Add explicit EADDRINUSE error handler in server.js to provide clear user messaging if port 3001 is occupied.",
            "6. Automated Verification: Execute Playwright automation suite to capture initial idle state, first fetch (Request #1), and repeated fetch (Request #2)."
        ],
        source_files=[
            SourceFileSpec(
                relative_path="server.js",
                language="javascript",
                description="Express server configuring port 3001, requestCount tracking, timestamping, and GET /api/student endpoint",
                role="Backend Express Server with State Counter"
            ),
            SourceFileSpec(
                relative_path="public/index.html",
                language="html",
                description="Client HTML interface with Fetch Data trigger and async/await fetch() DOM update routines",
                role="Client Fetch Interface & DOM Handler"
            ),
            SourceFileSpec(
                relative_path="package.json",
                language="json",
                description="Project package manifest declaring express dependency and start script",
                role="Package Configuration Manifest"
            )
        ],
        scenes=[
            ScreenshotScene(
                name="01_initial_idle_interface",
                title="Initial Idle State Prior to Data Retrieval",
                caption="Initial State — Client UI Delivered via HTTP GET on Port 3001 with No Student Data Loaded (http://localhost:3001/)",
                description=(
                    "Captures the initial state of the application after opening 'http://localhost:3001/'. "
                    "The Express server delivers 'index.html' via static middleware. Notice that no student data or timestamps "
                    "are pre-rendered; the interface displays an informative banner and an active 'Fetch Student Data' button, ready for user interaction."
                ),
                requirement_tag="Requirement 1: Static Asset Delivery",
                url_path="/",
                wait_selector="#fetchBtn",
                viewport={"width": 1440, "height": 850},
                actions=[
                    {"type": "wait_time", "ms": 500}
                ]
            ),
            ScreenshotScene(
                name="02_first_fetch_request_result",
                title="First On-Demand Fetch Request Execution (Request #1)",
                caption="First Connection — Browser Fetch API Retrieving Dynamic JSON Payload with Request #1 & Fresh Server Timestamp",
                description=(
                    "Illustrates the result of clicking 'Fetch Student Data' for the first time. The browser dispatches an asynchronous "
                    "HTTP GET request to '/api/student'. The Express server increments its internal counter to 1, stamps the current time, "
                    "and returns the student payload. The client dynamically renders the card showing 'Alex Kumar', 'CSE', Request '#1', and the timestamp."
                ),
                requirement_tag="Requirements 2 & 3: On-Demand Connection & Server Counter",
                url_path="/",
                wait_selector="#fetchBtn",
                viewport={"width": 1440, "height": 850},
                actions=[
                    {"type": "click", "selector": "#fetchBtn"},
                    {"type": "wait_time", "ms": 600}
                ]
            ),
            ScreenshotScene(
                name="03_second_fetch_counter_increment",
                title="Second On-Demand Fetch Request Proving Connection Increment",
                caption="Second Connection — Request Counter Incrementing to #2 Proving Discrete HTTP Connections Without Page Reload",
                description=(
                    "Demonstrates the on-demand connection behavior by triggering a second fetch request without refreshing the page. "
                    "The Express server increments its request counter to 2, generates a brand new timestamp, and responds. "
                    "The UI immediately updates to show Request '#2' and the new timestamp, proving each click creates a distinct HTTP connection."
                ),
                requirement_tag="Requirements 3 & 4: Discrete Connection & Dynamic DOM Updating",
                url_path="/",
                wait_selector="#fetchBtn",
                viewport={"width": 1440, "height": 850},
                actions=[
                    {"type": "click", "selector": "#fetchBtn"},
                    {"type": "wait_time", "ms": 800},
                    {"type": "click", "selector": "#fetchBtn"},
                    {"type": "wait_time", "ms": 600}
                ]
            )
        ],
        viva_questions=[
            {
                "question": "1. What does 'fetching data with a new connection' mean?",
                "answer": (
                    "It means that rather than receiving all data bundled during the initial page load, the browser establishes a brand new, "
                    "independent HTTP GET connection to the backend API endpoint on demand each time the user requests it, receiving fresh JSON data "
                    "without reloading the document."
                )
            },
            {
                "question": "2. How does the browser Fetch API differ from traditional form submissions?",
                "answer": (
                    "Traditional HTML form submissions trigger a full browser navigation cycle, causing the entire webpage to unload, refresh, "
                    "and re-render. The Fetch API is asynchronous; it transmits network requests in the background via JavaScript promises (async/await), "
                    "allowing specific DOM elements to update dynamically while maintaining active page state."
                )
            },
            {
                "question": "3. Where does the request counter live, and what happens if the server restarts?",
                "answer": (
                    "The request counter (let requestCount = 0) lives in the server process's RAM inside 'server.js'. It increments with every "
                    "incoming GET /api/student request. If the Node.js server process terminates or restarts, its memory resets and the counter begins at 0."
                )
            },
            {
                "question": "4. What is the role of res.json() in Express?",
                "answer": (
                    "res.json() automatically serializes a JavaScript object into a standard JSON string, sets the HTTP Content-Type header to "
                    "'application/json; charset=utf-8', and sends the response back to the client with an HTTP 200 status code."
                )
            },
            {
                "question": "5. How does client-side error handling work in fetchStudentData()?",
                "answer": (
                    "The function wraps the network call inside a try/catch/finally block. It verifies response.ok (throwing an Error if HTTP status "
                    "is not 2xx), catches network or server failures in the catch block to display user-friendly error banners, and utilizes the finally "
                    "block to always dismiss loading spinners and re-enable buttons."
                )
            }
        ],
        conclusion=(
            "Lab Assignment 5 was successfully implemented, verified, and demonstrated. The Express server and browser fetch client validated "
            "decoupled on-demand HTTP connections, dynamic server-side request counting and timestamping, and seamless asynchronous DOM updating "
            "with robust error handling."
        ),
        min_expected_pages=6
    ),

    # ==================== ASSIGNMENT 6: MONGODB AGGREGATIONS & EXPRESS REST API ====================
    6: AssignmentConfig(
        assignment_id=6,
        folder_name="Assignment-6",
        title="Lab Assignment 6: MongoDB Lookup, Aggregation Pipelines & Express REST API",
        subtitle="Relational NoSQL Joins ($lookup), Multi-Stage Pipelines & Native Driver CRUD Service",
        aim=(
            "To design and evaluate advanced database aggregations and RESTful web services in Node.js using the official native "
            "MongoDB driver (mongodb v6) without ORM abstractions, demonstrating: (1) multi-collection $lookup relational joins; "
            "(2) a complete Express REST API with unique index enforcement on rollNo; (3) $unwind array deconstruction with $group "
            "subject totals and averages; (4) filtered grouping ($match followed by $group) for scoring thresholds; and (5) multi-accumulator "
            "branch statistical aggregations ($avg, $max, $min) sorted descending."
        ),
        subject="Web Application Frameworks (WAF) Lab",
        department="Department of Computer Science & Engineering",
        institution="GITAM Deemed to be University",
        default_student_name="Jey",
        default_roll_no="9057",
        academic_year="2025-2026",
        server_type="express",
        server_dir="Assignment-6",
        server_command=["node", "api/server.js"],
        default_port=3002,
        entry_url="/",
        software_requirements=[
            "Operating System: Windows 10/11, macOS, or Linux",
            "Runtime: Node.js (v18+ LTS) and npm",
            "Database: MongoDB Community Server (v6+ active on 127.0.0.1:27017)",
            "Database Driver: Official MongoDB Node.js Native Driver (mongodb v6.12.0)",
            "Web Framework: Express.js (v4)",
            "Report Generation: Python 3.14 with Playwright, python-docx, Pillow, and pypdfium2"
        ],
        faculty_requirements=[
            {
                "requirement": "1. MongoDB $lookup Join",
                "implementation": "scripts/lookup-students.js",
                "evidence": "$lookup joining students.departmentId with departments._id, followed by $unwind to flatten the joined department object."
            },
            {
                "requirement": "2. Express REST API with Native Driver",
                "implementation": "api/server.js",
                "evidence": "Complete CRUD REST endpoints (GET /students, GET /students/:rollNo, POST /students, PUT /students/:rollNo, DELETE /students/:rollNo) with unique index validation on port 3002."
            },
            {
                "requirement": "3. $unwind & $group for Subject Summaries",
                "implementation": "scripts/subject-summary.js",
                "evidence": "$unwind on nested 'subjects' array followed by $group calculating totalMarks ($sum) and averageMarks ($avg) per student."
            },
            {
                "requirement": "4. $match & $group for High Scorers (> 60)",
                "implementation": "scripts/branch-above-60.js",
                "evidence": "$match filtering students with marks > 60 followed by $group counting qualifying students by branch."
            },
            {
                "requirement": "5. Branch Statistics ($avg, $max, $min)",
                "implementation": "scripts/branch-statistics.js",
                "evidence": "$group computing average, maximum, and minimum marks per branch with $round and $sort({ averageMarks: -1 })."
            }
        ],
        procedure_steps=[
            "1. Database Environment Initialization: Ensure local MongoDB service is running at 127.0.0.1:27017 targeting dedicated database 'waf_assignment_6'.",
            "2. Idempotent Database Seeding: Execute 'scripts/seed.js' to create unique index on students(rollNo) and populate departments and students collections with deterministic ObjectIds.",
            "3. $lookup Relational Join Implementation: Author 'scripts/lookup-students.js' implementing four-stage aggregation ($lookup, $unwind, $project, $sort).",
            "4. Express REST API Development: Author 'api/server.js' configuring Express on port 3002 with native MongoClient connection pooling and CRUD route handlers.",
            "5. Array Deconstruction & Grouping: Implement 'scripts/subject-summary.js' utilizing $unwind on nested arrays and computing $sum and $avg accumulators.",
            "6. Filtered Grouping & Branch Statistics: Implement 'scripts/branch-above-60.js' and 'scripts/branch-statistics.js' to compute conditional counts and sorted branch metrics.",
            "7. Empirical Verification: Execute automated script runners and browser tests to capture console tables and REST API responses."
        ],
        source_files=[
            SourceFileSpec(
                relative_path="api/server.js",
                language="javascript",
                description="Express REST API providing full student CRUD services on port 3002 using native MongoDB driver",
                role="Requirement 2: Express REST API"
            ),
            SourceFileSpec(
                relative_path="scripts/seed.js",
                language="javascript",
                description="Idempotent database seeder creating collections, unique indexes, and 8 realistic student records",
                role="Database Seeder & Index Setup"
            ),
            SourceFileSpec(
                relative_path="scripts/lookup-students.js",
                language="javascript",
                description="MongoDB aggregation script executing $lookup relational join between students and departments",
                role="Requirement 1: $lookup Aggregation"
            ),
            SourceFileSpec(
                relative_path="scripts/subject-summary.js",
                language="javascript",
                description="MongoDB aggregation script using $unwind and $group to calculate total and average subject marks",
                role="Requirement 3: $unwind & $group"
            ),
            SourceFileSpec(
                relative_path="scripts/branch-above-60.js",
                language="javascript",
                description="MongoDB aggregation script combining $match filter (marks > 60) with $group branch count",
                role="Requirement 4: $match & $group"
            ),
            SourceFileSpec(
                relative_path="scripts/branch-statistics.js",
                language="javascript",
                description="MongoDB aggregation script computing branch average, maximum, and minimum marks sorted descending",
                role="Requirement 5: Branch Statistics"
            ),
            SourceFileSpec(
                relative_path="package.json",
                language="json",
                description="Project package manifest declaring express and mongodb driver dependencies with script shortcuts",
                role="Project Metadata & Dependency Manifest"
            )
        ],
        scenes=[
            ScreenshotScene(
                name="01_api_root_manifest",
                title="Express REST API Root Endpoint Documentation",
                caption="API Documentation Route — GET / Listing Supported Student Endpoints, Port, and Database (http://localhost:3002/)",
                description=(
                    "Captures the root endpoint ('/') of the Express REST API service on port 3002. "
                    "The service confirms active connection to 'waf_assignment_6' and delivers a structured JSON manifest "
                    "documenting all supported routes (GET /students, GET /students/:rollNo, POST /students, PUT /students/:rollNo, DELETE /students/:rollNo)."
                ),
                requirement_tag="Requirement 2: Express REST API Service",
                url_path="/",
                viewport={"width": 1440, "height": 750},
                actions=[
                    {"type": "wait_time", "ms": 500}
                ]
            ),
            ScreenshotScene(
                name="02_api_students_json_list",
                title="Live MongoDB Student Records via REST API",
                caption="REST API Query — GET /students Delivering Live Documents from MongoDB 'waf_assignment_6' Database",
                description=(
                    "Displays the live JSON payload returned by 'http://localhost:3002/students'. "
                    "The Express route handler executes studentsCol.find({}).sort({ rollNo: 1 }).toArray(), "
                    "streaming all eight seeded student documents from MongoDB to the client with HTTP 200 OK."
                ),
                requirement_tag="Requirement 2: REST API Database Query",
                url_path="/students",
                viewport={"width": 1440, "height": 750},
                actions=[
                    {"type": "wait_time", "ms": 500}
                ]
            )
        ],
        cli_commands=[
            CliCommandSpec(
                name="03_seed_execution",
                title="Idempotent Database Seeder Execution",
                caption="Database Seeding — Unique Index Creation on rollNo & Sample Population of 'waf_assignment_6'",
                description=(
                    "Demonstrates execution of 'scripts/seed.js'. The script connects to MongoDB, establishes a unique index "
                    "on students(rollNo) to prevent duplicates, and idempotently populates three departments and eight student records."
                ),
                requirement_tag="Database Infrastructure & Index Setup",
                command=["node", "scripts/seed.js"]
            ),
            CliCommandSpec(
                name="04_req1_lookup_students",
                title="Requirement 1: $lookup Relational Join Pipeline",
                caption="Aggregation Pipeline 1 — $lookup & $unwind Joining Students with Department Names and HODs",
                description=(
                    "Executes 'scripts/lookup-students.js'. Validates the multi-collection $lookup stage joining "
                    "students.departmentId to departments._id, followed by $unwind to flatten the joined array into an object."
                ),
                requirement_tag="Requirement 1: $lookup Aggregation",
                command=["node", "scripts/lookup-students.js"]
            ),
            CliCommandSpec(
                name="05_req3_subject_summary",
                title="Requirement 3: $unwind and $group on Subject Arrays",
                caption="Aggregation Pipeline 3 — $unwind Deconstructing Nested Arrays & $group Calculating Total/Average Marks",
                description=(
                    "Executes 'scripts/subject-summary.js'. Demonstrates $unwind splitting each student's subjects array into individual "
                    "document rows, allowing $group to compute totalMarks ($sum) and averageMarks ($avg) per student."
                ),
                requirement_tag="Requirement 3: $unwind & $group",
                command=["node", "scripts/subject-summary.js"]
            ),
            CliCommandSpec(
                name="06_req4_branch_above_60",
                title="Requirement 4: $match Filter Combined with $group",
                caption="Aggregation Pipeline 4 — $match Filtering Marks > 60 & $group Counting Qualifying Students per Branch",
                description=(
                    "Executes 'scripts/branch-above-60.js'. Demonstrates pipeline optimization by applying $match early to filter "
                    "only students with marks > 60 before passing the reduced working set to $group for branch counting."
                ),
                requirement_tag="Requirement 4: $match & $group",
                command=["node", "scripts/branch-above-60.js"]
            ),
            CliCommandSpec(
                name="07_req5_branch_statistics",
                title="Requirement 5: Branch Statistical Aggregation",
                caption="Aggregation Pipeline 5 — Multi-Accumulator Aggregation ($avg, $max, $min) Sorted Descending",
                description=(
                    "Executes 'scripts/branch-statistics.js'. Groups students by branch and computes average marks ($avg), "
                    "maximum marks ($max), and minimum marks ($min), formatted with $round and sorted in descending order of performance."
                ),
                requirement_tag="Requirement 5: Branch Statistics",
                command=["node", "scripts/branch-statistics.js"]
            )
        ],
        viva_questions=[
            {
                "question": "1. What is the MongoDB Aggregation Pipeline?",
                "answer": (
                    "The aggregation pipeline is a framework for data processing modeled on the concept of data processing pipelines. "
                    "Documents enter a multi-stage pipeline where each stage (such as $match, $lookup, $unwind, $group, and $sort) transforms "
                    "the documents as they pass through, executing calculations directly inside the database engine."
                )
            },
            {
                "question": "2. How does the $lookup stage work in MongoDB?",
                "answer": (
                    "The $lookup stage performs a left outer join between two collections in the same database. It matches documents from the "
                    "input collection with documents from the 'from' collection using 'localField' and 'foreignField', outputting matched records "
                    "as a new array field in each document."
                )
            },
            {
                "question": "3. What is the role of the $unwind stage?",
                "answer": (
                    "$unwind deconstructs an array field from the input documents to output a document for each element in the array. "
                    "This is essential for flattening arrays produced by $lookup or calculating aggregations across nested sub-document arrays."
                )
            },
            {
                "question": "4. Why is placing $match early in the pipeline considered best practice?",
                "answer": (
                    "Placing $match as early as possible filters out non-qualifying documents immediately, drastically reducing the volume "
                    "of data that subsequent stages ($lookup, $unwind, $group) must process in memory. It also enables MongoDB to leverage database indexes."
                )
            },
            {
                "question": "5. Why use the official MongoDB Native Driver instead of Mongoose in this practical?",
                "answer": (
                    "The native driver (mongodb v6) provides direct, unmediated access to MongoDB's wire protocol and cursor APIs without the "
                    "overhead, schema caching, and abstraction layers of Mongoose. It gives complete transparency into raw NoSQL operations and aggregation pipelines."
                )
            }
        ],
        conclusion=(
            "Lab Assignment 6 was successfully implemented and verified against a live local MongoDB instance. All five core requirements—"
            "relational NoSQL $lookup joins, a complete Express REST API service with unique index validation, $unwind array processing, "
            "filtered grouping, and multi-accumulator branch statistics—were empirically proven through automated execution."
        ),
        min_expected_pages=15
    ),

    # ==================== ASSIGNMENT 7: MONGODB QUERIES, CURSORS & ATOMIC UPDATES ====================
    7: AssignmentConfig(
        assignment_id=7,
        folder_name="Assignment-7",
        title="Lab Assignment 7: MongoDB Queries, Cursor Chaining, Regex & Atomic Updates",
        subtitle="Cursor sort/limit, BSON ObjectId Lookups, Filtered Deletion, Regex & Atomic Inventory Concurrency",
        aim=(
            "To evaluate essential MongoDB queries, cursor methods, BSON data typing, and concurrency patterns in Node.js "
            "using the official native MongoDB driver, demonstrating: (1) cursor chaining with sort() and limit() for top-K scorers "
            "with deterministic tie-breaking; (2) 12-byte BSON ObjectId primary key resolution; (3) safe filtered deletion (deleteMany "
            "with marks < 40); (4) database-side case-insensitive regular expression pattern matching ($regex: '^M'); and (5) atomic "
            "inventory concurrency control in a library management system using findOneAndUpdate with atomic $inc operators."
        ),
        subject="Web Application Frameworks (WAF) Lab",
        department="Department of Computer Science & Engineering",
        institution="GITAM Deemed to be University",
        default_student_name="Jey",
        default_roll_no="9057",
        academic_year="2025-2026",
        server_type="none",
        software_requirements=[
            "Operating System: Windows 10/11, macOS, or Linux",
            "Runtime: Node.js (v18+ LTS) and npm",
            "Database: MongoDB Community Server (v6+ active on 127.0.0.1:27017)",
            "Database Driver: Official MongoDB Node.js Native Driver (mongodb v6.12.0)",
            "Report Generation: Python 3.14 with Playwright, python-docx, Pillow, and pypdfium2"
        ],
        faculty_requirements=[
            {
                "requirement": "6. Top 3 Scorers via sort() & limit()",
                "implementation": "scripts/top-three.js",
                "evidence": "Cursor chaining find({}).sort({ marks: -1, rollNo: 1 }).limit(3) returning top scorers with tie-breaking."
            },
            {
                "requirement": "7. Document Lookup by BSON ObjectId",
                "implementation": "scripts/find-by-id.js",
                "evidence": "Primary key query using new ObjectId('65f1b2b2b2b2b2b2b2b2b102') demonstrating 12-byte binary BSON resolution."
            },
            {
                "requirement": "8. Filtered Deletion Below 40 Marks",
                "implementation": "scripts/delete-below-40.js",
                "evidence": "Safe destructive deletion using deleteMany({ marks: { $lt: 40 } }) with confirmation safeguards."
            },
            {
                "requirement": "9. Case-Insensitive Regex Pattern Matching",
                "implementation": "scripts/names-starting-m.js",
                "evidence": "Database pattern query find({ name: { $regex: '^M', $options: 'i' } }) identifying matching student names."
            },
            {
                "requirement": "10. Atomic Library Inventory Management",
                "implementation": "scripts/library-management.js",
                "evidence": "Atomic issue and return operations using findOneAndUpdate with $inc: { copies: -1/+1 } and { copies: { $gt: 0 } } race-condition guards."
            }
        ],
        procedure_steps=[
            "1. Database Environment Initialization: Ensure local MongoDB service is active on 127.0.0.1:27017 targeting dedicated database 'waf_assignment_7'.",
            "2. Idempotent Database Seeding: Execute 'scripts/seed.js' populating departments, students, and library books collections with deterministic ObjectIds.",
            "3. Top-K Scorers Query: Author 'scripts/top-three.js' utilizing cursor methods find(), sort({ marks: -1 }), and limit(3) with projection.",
            "4. BSON ObjectId Resolution: Implement 'scripts/find-by-id.js' instantiating new ObjectId(...) to retrieve specific student documents.",
            "5. Safe Destructive Deletion: Author 'scripts/delete-below-40.js' with interactive or automated safeguard flags executing deleteMany({ marks: { $lt: 40 } }).",
            "6. Regex Pattern Matching: Implement 'scripts/names-starting-m.js' executing case-insensitive regular expression matching on student names.",
            "7. Atomic Concurrency Management: Build 'scripts/library-management.js' implementing atomic book checkout and checkin with positive inventory guards.",
            "8. Empirical Verification: Execute test suite across all six scripts and capture genuine terminal output evidence."
        ],
        source_files=[
            SourceFileSpec(
                relative_path="scripts/seed.js",
                language="javascript",
                description="Database seeder populating departments, students, and library books with unique indexes",
                role="Database Seeder & Index Setup"
            ),
            SourceFileSpec(
                relative_path="scripts/top-three.js",
                language="javascript",
                description="Cursor chaining script retrieving top 3 student scorers using sort() and limit()",
                role="Requirement 6: Cursor sort() & limit()"
            ),
            SourceFileSpec(
                relative_path="scripts/find-by-id.js",
                language="javascript",
                description="BSON primary key lookup script demonstrating new ObjectId('...') resolution",
                role="Requirement 7: BSON ObjectId Lookup"
            ),
            SourceFileSpec(
                relative_path="scripts/delete-below-40.js",
                language="javascript",
                description="Safe destructive deletion script removing student records below 40 marks with confirmation guards",
                role="Requirement 8: Filtered Deletion"
            ),
            SourceFileSpec(
                relative_path="scripts/names-starting-m.js",
                language="javascript",
                description="Database pattern matching script querying names starting with 'M' using case-insensitive $regex",
                role="Requirement 9: Regular Expression Query"
            ),
            SourceFileSpec(
                relative_path="scripts/library-management.js",
                language="javascript",
                description="Library management program implementing atomic book issue/return concurrency using findOneAndUpdate and $inc",
                role="Requirement 10: Atomic Concurrency & Inventory"
            ),
            SourceFileSpec(
                relative_path="package.json",
                language="json",
                description="Project package manifest declaring mongodb driver dependency and script shortcuts",
                role="Project Metadata & Dependency Manifest"
            )
        ],
        cli_commands=[
            CliCommandSpec(
                name="01_seed_execution",
                title="Idempotent Database Seeder Execution",
                caption="Database Seeding — Unique Index Setup and Data Population for 'waf_assignment_7'",
                description=(
                    "Demonstrates execution of 'scripts/seed.js'. Populates departments, students, and library book collections "
                    "with deterministic test data and creates unique indexes on students(rollNo) and books(title)."
                ),
                requirement_tag="Database Infrastructure & Index Setup",
                command=["node", "scripts/seed.js"]
            ),
            CliCommandSpec(
                name="02_req6_top_three",
                title="Requirement 6: Top 3 Scorers via sort() & limit()",
                caption="Cursor Chaining — sort({ marks: -1 }) & limit(3) with Deterministic Tie-Breaking",
                description=(
                    "Executes 'scripts/top-three.js'. Validates cursor chaining on the database server to retrieve "
                    "the top 3 scoring students (Meera Nair 94, Pooja Reddy 91, Aarav Sharma 88) with minimal network transfer."
                ),
                requirement_tag="Requirement 6: Cursor sort() & limit()",
                command=["node", "scripts/top-three.js"]
            ),
            CliCommandSpec(
                name="03_req7_find_by_id",
                title="Requirement 7: Document Lookup by BSON ObjectId",
                caption="Primary Key Query — Resolving 12-Byte Binary BSON new ObjectId('65f1b2b2b2b2b2b2b2b2b102')",
                description=(
                    "Executes 'scripts/find-by-id.js'. Demonstrates BSON primary key resolution by converting a 24-character "
                    "hex string into a binary 12-byte ObjectId to retrieve Meera Nair's complete student record."
                ),
                requirement_tag="Requirement 7: BSON ObjectId Lookup",
                command=["node", "scripts/find-by-id.js"]
            ),
            CliCommandSpec(
                name="04_req8_delete_below_40",
                title="Requirement 8: Filtered Deletion of Records Below 40",
                caption="Destructive Deletion — deleteMany({ marks: { $lt: 40 } }) with Confirmation Safeguards",
                description=(
                    "Executes 'scripts/delete-below-40.js' with the '--yes' confirmation flag. Identifies and removes "
                    "two student records scoring below 40 marks (Rohan Varma 35 and Suresh Iyer 38), reporting deletedCount: 2."
                ),
                requirement_tag="Requirement 8: Filtered Deletion",
                command=["node", "scripts/delete-below-40.js", "--yes"]
            ),
            CliCommandSpec(
                name="05_req9_names_starting_m",
                title="Requirement 9: Case-Insensitive Regex Pattern Matching",
                caption="Pattern Matching Query — find({ name: { $regex: '^M', $options: 'i' } })",
                description=(
                    "Executes 'scripts/names-starting-m.js'. Demonstrates database-side regex pattern evaluation to find "
                    "all students whose names begin with the letter 'M' (Meera Nair and Manish Gupta)."
                ),
                requirement_tag="Requirement 9: Regex Pattern Matching",
                command=["node", "scripts/names-starting-m.js"]
            ),
            CliCommandSpec(
                name="06_req10_library_issue",
                title="Requirement 10: Atomic Library Book Issue Operation",
                caption="Atomic Inventory Concurrency — findOneAndUpdate with $inc: { copies: -1 } and { copies: { $gt: 0 } }",
                description=(
                    "Executes 'scripts/library-management.js issue \"Clean Code\"'. Demonstrates an atomic "
                    "checkout operation using findOneAndUpdate to decrement available inventory while preventing negative inventory under concurrency."
                ),
                requirement_tag="Requirement 10: Atomic Concurrency & Library System",
                command=["node", "scripts/library-management.js", "issue", "Clean Code"]
            )
        ],
        viva_questions=[
            {
                "question": "1. What is a MongoDB Cursor and why is cursor chaining efficient?",
                "answer": (
                    "A cursor is a pointer to the result set of a query on the database server. Methods like sort() and limit() "
                    "do not execute immediately in client memory; they modify the query plan on the server. When toArray() or next() is called, "
                    "MongoDB executes the entire optimized pipeline on the database engine and transfers only the final qualifying documents across the network."
                )
            },
            {
                "question": "2. Why is new ObjectId('...') required when querying by _id in Node.js?",
                "answer": (
                    "MongoDB stores the _id primary key as a 12-byte binary BSON ObjectId, not as a plain JavaScript UTF-8 string. "
                    "Querying with { _id: '65f1b2b2...' } fails because a string data type never matches a BSON binary type. "
                    "We must instantiate new ObjectId('...') using the native driver to construct the binary representation."
                )
            },
            {
                "question": "3. How does findOneAndUpdate provide atomic concurrency in the library system?",
                "answer": (
                    "In multi-user web applications, checking available copies and updating them in two separate steps introduces a race condition "
                    "where two users can borrow the last copy simultaneously. findOneAndUpdate executes the read and the update as a single, "
                    "indivisible atomic operation on the database server. The query filter { title: ..., copies: { $gt: 0 } } guarantees copies cannot drop below zero."
                )
            },
            {
                "question": "4. What is the difference between deleteOne() and deleteMany()?",
                "answer": (
                    "deleteOne() removes at most the first document that matches the query criteria. deleteMany() removes all documents that match "
                    "the query criteria. In Requirement 8, deleteMany({ marks: { $lt: 40 } }) ensures every failing student record is removed across the collection."
                )
            },
            {
                "question": "5. What are the options available with MongoDB regular expressions?",
                "answer": (
                    "MongoDB supports regex options including 'i' for case-insensitivity, 'm' for multi-line matching, 'x' to ignore whitespace in patterns, "
                    "and 's' (dotAll) to allow the dot metacharacter to match newline characters. In Requirement 9, { $options: 'i' } ensures both 'M' and 'm' match."
                )
            }
        ],
        conclusion=(
            "Lab Assignment 7 was successfully implemented and verified against a live local MongoDB instance. Cursor chaining (sort and limit), "
            "BSON ObjectId primary key lookup, safe filtered deletion, regular expression matching, and race-condition-free atomic library inventory "
            "concurrency control were empirically demonstrated."
        ),
        min_expected_pages=15
    )
}


def get_assignment_config(assignment_id: int) -> AssignmentConfig:
    """Retrieve configuration for a given assignment number."""
    if assignment_id not in ASSIGNMENT_REGISTRY:
        raise ValueError(
            f"Assignment {assignment_id} is not configured yet. "
            f"Available assignments in registry: {list(ASSIGNMENT_REGISTRY.keys())}. "
            f"You can add Assignment {assignment_id} to ASSIGNMENT_REGISTRY in config.py."
        )
    return ASSIGNMENT_REGISTRY[assignment_id]


def list_supported_assignments() -> List[Dict[str, Any]]:
    """Return summary metadata for all supported assignments."""
    summaries = []
    for aid, cfg in sorted(ASSIGNMENT_REGISTRY.items()):
        summaries.append({
            "assignment_id": aid,
            "folder_name": cfg.folder_name,
            "title": cfg.title,
            "subtitle": cfg.subtitle,
            "server_type": cfg.server_type,
            "default_port": cfg.default_port,
            "scene_count": len(cfg.scenes),
            "cli_command_count": len(cfg.cli_commands),
            "source_file_count": len(cfg.source_files),
            "min_expected_pages": cfg.min_expected_pages
        })
    return summaries


def validate_assignment_config(config: AssignmentConfig, workspace_root: Path) -> Tuple[bool, List[str]]:
    """
    Validate that an assignment's configuration is complete and that all referenced
    folders and source files actually exist on disk.
    """
    errors: List[str] = []
    workspace_root = Path(workspace_root).resolve()

    # 1. Validate folder existence
    assignment_dir = workspace_root / config.folder_name
    if not assignment_dir.is_dir():
        errors.append(f"Assignment folder '{config.folder_name}' not found at {assignment_dir}")

    # 2. Validate required metadata
    if not config.title:
        errors.append("Assignment title is empty.")
    if not config.aim:
        errors.append("Assignment aim is empty.")
    if not config.conclusion:
        errors.append("Assignment conclusion is empty.")

    # 3. Validate source files exist on disk
    if not config.source_files:
        errors.append("No source files configured for code appendix.")
    else:
        for sf in config.source_files:
            file_path = assignment_dir / sf.relative_path
            if not file_path.exists():
                errors.append(f"Referenced source file missing on disk: {file_path}")

    # 4. Validate evidence configuration
    if not config.scenes and not config.cli_commands:
        errors.append("Assignment has neither browser scenes nor CLI commands configured.")

    return len(errors) == 0, errors
