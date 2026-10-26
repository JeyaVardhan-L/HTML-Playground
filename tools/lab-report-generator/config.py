"""
Configuration and Registry for WAF Lab Report Generator.
Defines metadata, server start commands, source files, and test automation scenes
for Assignment 2 and prepares extensible structure for Assignments 3 through 7.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
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
    server_type: str = "static_http"  # static_http, express, vite, custom
    server_dir: Optional[str] = None
    server_command: Optional[List[str]] = None
    default_port: int = 8000
    entry_url: str = "/index.html"
    software_requirements: List[str] = field(default_factory=list)
    faculty_requirements: List[Dict[str, str]] = field(default_factory=list)
    procedure_steps: List[str] = field(default_factory=list)
    source_files: List[SourceFileSpec] = field(default_factory=list)
    scenes: List[ScreenshotScene] = field(default_factory=list)
    viva_questions: List[Dict[str, str]] = field(default_factory=list)
    conclusion: str = ""


# Registry of supported assignments
ASSIGNMENT_REGISTRY: Dict[int, AssignmentConfig] = {
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
            "Report Generation: Python 3.14 with Playwright, python-docx, and Pillow"
        ],
        faculty_requirements=[
            {
                "requirement": "1. Create Frames",
                "implementation": "index.html & js/script.js",
                "evidence": "<iframe src='home.html' name='content' id='content-frame'> with navigation <a href='...' target='content'> and bidirectional postMessage height auto-resizing."
            },
            {
                "requirement": "2. Header, Footer, Articles",
                "implementation": "All HTML documents",
                "evidence": "Semantic HTML5 tags: <header role='banner'>, <footer role='contentinfo'>, <section>, and <article class='article-section'> defining document hierarchy."
            },
            {
                "requirement": "3. Form in Tabular Format",
                "implementation": "survey.html & js/script.js",
                "evidence": "<table class='form-table'> pairing labels in the left column with inputs, selects, radio groups, checkboxes, and textareas in the right column, plus DOM validation."
            },
            {
                "requirement": "4. Hyperlinks",
                "implementation": "All HTML documents",
                "evidence": "Three distinct link targets: target='content' (loads inside iframe), target='_top' (breaks out of iframe), and target='_blank' (external docs)."
            },
            {
                "requirement": "5. CSS Properties",
                "implementation": "css/style.css",
                "evidence": "Grayscale CSS custom properties (--background: #f5f5f7; --surface: #ffffff; --border: #d2d2d7), Flexbox, CSS Grid, and macOS system typography."
            },
            {
                "requirement": "6. Responsive Design",
                "implementation": "css/style.css",
                "evidence": "Fluid layouts, table horizontal overflow wrappers, and @media (max-width: 768px) media queries converting tabular form cells into stacked mobile blocks."
            }
        ],
        procedure_steps=[
            "1. Architectural Layout Design: Structured 'index.html' as the master parent shell comprising a fixed minimalist top header with brand title, horizontal navigation bar, named <iframe> viewport, and academic footer.",
            "2. Modular Subpage Authoring: Implemented dedicated subpages: 'home.html' (model family grid cards), 'models.html' (tabular model comparison matrix), 'survey.html' (developer feedback form), 'articles.html' (semantic technical articles), and 'resources.html' (compliance matrix).",
            "3. Tabular Form Implementation: Engineered 'survey.html' following the faculty requirement of tabular form structure (<table class='form-table'>), with left-aligned label cells and right-aligned input cells incorporating text, email, select dropdowns, radio buttons, checkboxes, and textareas.",
            "4. Dynamic Scripting & Auto-Height Sync: Developed 'js/script.js' to handle seamless iframe height synchronisation via window.postMessage, live client-side table search filtering in 'models.html', and form validation with summary card presentation in 'survey.html'.",
            "5. Design System & CSS Styling: Built 'css/style.css' adhering strictly to an Apple-inspired grayscale palette, eliminating bright neons and glows in favor of subtle 1px borders, smooth card corners, and native system fonts.",
            "6. Responsive Viewport Adaptation: Enforced mobile responsiveness using CSS media queries (@media (max-width: 768px)) that stack navigation items, collapse comparison tables, and transform table cells into block-level elements.",
            "7. Local Server Hosting & Cross-Origin Verification: Served the project through Python's built-in HTTP server to ensure clean same-origin iframe communication and smooth script execution.",
            "8. Automated Verification & Capture: Executed Playwright automated headless Chromium browsing to systematically navigate all routes, test search filters and form validation, capture evidence screenshots, and verify complete compliance."
        ],
        source_files=[
            SourceFileSpec("index.html", "html", "Master parent shell containing header, horizontal navigation bar, named iframe, and footer", "Parent Frame Shell"),
            SourceFileSpec("home.html", "html", "Introductory home page showcasing foundation AI model families in a clean CSS grid", "Home Overview Page"),
            SourceFileSpec("models.html", "html", "Comprehensive comparison table of leading frontier AI models with live search filter", "Model Comparison Matrix"),
            SourceFileSpec("survey.html", "html", "Developer survey form organized strictly in an HTML table with validation and summary display", "Tabular Developer Survey"),
            SourceFileSpec("articles.html", "html", "Semantic technical deep-dives covering scale, reasoning, multimodality, agents, and limitations", "Technical Articles"),
            SourceFileSpec("resources.html", "html", "Assignment compliance verification matrix, official model documentation links, and viva guide", "Resources & Viva Guide"),
            SourceFileSpec("css/style.css", "css", "Unified minimalist Apple-inspired grayscale stylesheet with design tokens, grid, and media queries", "Master Stylesheet"),
            SourceFileSpec("js/script.js", "js", "JavaScript logic for parent iframe communication, auto-height resizing, live search filter, and form validation", "Client Interactivity Script")
        ],
        scenes=[
            ScreenshotScene(
                name="01_parent_shell_home",
                title="Master Parent Frame and Home Page Grid View",
                caption="Frontier AI Atlas — Master Parent Frame (index.html) Hosting the Home Page Grid View (home.html)",
                description=(
                    "Demonstrates the primary parent layout containing the compact top header, "
                    "active 'Home' navigation tab, and the named iframe element (<iframe name='content'>) "
                    "rendering the responsive 6-card grid of modern frontier AI models (OpenAI, Anthropic, Google DeepMind, "
                    "Meta, DeepSeek, and Mistral). Fulfills Requirement 1 (Frames) and Requirement 2 (Header/Footer)."
                ),
                requirement_tag="Requirement 1: Frames & Requirement 2: Header/Footer",
                url_path="/index.html",
                wait_selector="#content-frame",
                viewport={"width": 1440, "height": 950},
                actions=[
                    {"type": "wait_time", "ms": 1000}
                ]
            ),
            ScreenshotScene(
                name="02_models_explorer_table",
                title="Model Explorer Comparison Table Matrix",
                caption="Model Explorer Page (models.html) — Tabular Comparison Matrix of Frontier AI Models",
                description=(
                    "Displays the Model Explorer table loaded seamlessly inside the parent frame via target='content'. "
                    "The clean four-column table outlines Organization, Model Family, Primary Capabilities, and Official Documentation. "
                    "Fulfills Requirement 1 (Frames), Requirement 4 (Hyperlinks), and Requirement 5 (Grayscale CSS)."
                ),
                requirement_tag="Requirement 1: Frames & Requirement 5: CSS Properties",
                url_path="/index.html",
                wait_selector="#nav-models",
                viewport={"width": 1440, "height": 950},
                actions=[
                    {"type": "click", "selector": "#nav-models"},
                    {"type": "wait_time", "ms": 1000}
                ]
            ),
            ScreenshotScene(
                name="03_models_search_interaction",
                title="Live Search Filtering in Model Explorer",
                caption="Live Search Filtering in Model Explorer — Dynamic DOM Manipulation for Filtered Model Subsets",
                description=(
                    "Demonstrates the real-time search filter in action. Entering 'reasoning' into the search input "
                    "filters table rows dynamically via JavaScript DOM manipulation, displaying matching models "
                    "(OpenAI GPT-4o/o1 and DeepSeek V3/R1) and updating the live match counter ('Showing 2 of 6 models'). "
                    "Proves interactive client-side scripting and clean UI feedback."
                ),
                requirement_tag="Requirement 5: CSS Properties & Client JavaScript",
                url_path="/index.html",
                wait_selector="#nav-models",
                viewport={"width": 1440, "height": 950},
                actions=[
                    {"type": "click", "selector": "#nav-models"},
                    {"type": "wait_time", "ms": 500},
                    {"type": "iframe_action", "frame_selector": "#content-frame", "sub_action": {
                        "type": "fill", "selector": "#modelSearch", "value": "reasoning"
                    }},
                    {"type": "wait_time", "ms": 800}
                ]
            ),
            ScreenshotScene(
                name="04_developer_survey_initial",
                title="Developer Survey Form in Strict Tabular Format",
                caption="Developer Survey (survey.html) — Form Created in Tabular Format (<table class='form-table'>)",
                description=(
                    "Presents the developer survey form designed in strict accordance with Faculty Requirement 3. "
                    "Every form row (<tr class='form-row'>) contains a label cell (<td class='form-label-cell'>) "
                    "paired with an input cell (<td class='form-input-cell'>) encompassing text inputs, email verification, "
                    "custom styled selects, radio button groups, checkboxes, and textareas."
                ),
                requirement_tag="Requirement 3: Form in Tabular Format",
                url_path="/index.html",
                wait_selector="#nav-survey",
                viewport={"width": 1440, "height": 1050},
                actions=[
                    {"type": "click", "selector": "#nav-survey"},
                    {"type": "wait_time", "ms": 1000}
                ]
            ),
            ScreenshotScene(
                name="05_developer_survey_submitted",
                title="Survey Form Submission and Dynamic Response Summary",
                caption="Survey Form Submission & Validation — Client-Side Verification and Dynamic Result Summary",
                description=(
                    "Illustrates successful form validation and dynamic summary output card generation. "
                    "The form was populated with test data (Student: Jey, Email: student@gitam.in, Model: Anthropic Claude 3.5 Sonnet, "
                    "Experience: Advanced) and submitted. The event handler intercepted submission via event.preventDefault(), "
                    "validated all mandatory fields, displayed the formatted response summary card, and triggered postMessage "
                    "to auto-expand the parent frame height."
                ),
                requirement_tag="Requirement 3: Tabular Form Validation & Dynamic DOM Summary",
                url_path="/index.html",
                wait_selector="#nav-survey",
                viewport={"width": 1440, "height": 1350},
                actions=[
                    {"type": "click", "selector": "#nav-survey"},
                    {"type": "wait_time", "ms": 500},
                    {"type": "iframe_action", "frame_selector": "#content-frame", "sub_action": {
                        "type": "fill_survey",
                        "name": "Jey",
                        "email": "student@gitam.in",
                        "model": "Anthropic Claude 3.5 Sonnet",
                        "use_case": "Software Engineering & Coding",
                        "experience": "Advanced",
                        "capabilities": ["Code Generation", "Test-Time Reasoning"],
                        "comments": "Frontier AI Atlas verified for WAF Lab Assignment 2."
                    }},
                    {"type": "wait_time", "ms": 1000}
                ]
            ),
            ScreenshotScene(
                name="06_semantic_articles_view",
                title="Semantic Technical Articles Hierarchy",
                caption="Semantic Articles Page (articles.html) — Document Hierarchy (<article>, <section>, <header>)",
                description=(
                    "Highlights the structural implementation of Faculty Requirement 2. The page utilizes semantic "
                    "HTML5 tags (<header>, <main>, <section>, <article class='article-section'>) to organize detailed "
                    "discussions on compute scaling laws, test-time reasoning architectures, and agentic workflows "
                    "without redundant non-semantic <div> tags."
                ),
                requirement_tag="Requirement 2: Header, Footer, Articles",
                url_path="/index.html",
                wait_selector="#nav-articles",
                viewport={"width": 1440, "height": 1000},
                actions=[
                    {"type": "click", "selector": "#nav-articles"},
                    {"type": "wait_time", "ms": 1000}
                ]
            ),
            ScreenshotScene(
                name="07_resources_and_compliance",
                title="Requirements Compliance Matrix and Viva Guide",
                caption="Resources & Compliance Matrix (resources.html) — Faculty Requirements Verification & Viva Prep",
                description=(
                    "Displays the project verification matrix, linking each faculty requirement to the precise "
                    "source file, lines of code, and architectural pattern. Also features external documentation links "
                    "(target='_blank') and lab viva voce preparation questions."
                ),
                requirement_tag="Requirement 4: Hyperlinks & Viva Documentation",
                url_path="/index.html",
                wait_selector="#nav-resources",
                viewport={"width": 1440, "height": 1000},
                actions=[
                    {"type": "click", "selector": "#nav-resources"},
                    {"type": "wait_time", "ms": 1000}
                ]
            ),
            ScreenshotScene(
                name="08_mobile_responsive_view",
                title="Fluid Responsive Adaptation on Mobile Viewport",
                caption="Responsive Mobile Emulation (375x667 Viewport) — Fluid Adaptation and Mobile-Optimized Form",
                description=(
                    "Demonstrates the responsive CSS design system on a simulated mobile viewport (iPhone SE, 375x667). "
                    "The horizontal navigation bar wraps cleanly, content cards stack into a single column, "
                    "and table cells convert from tabular display to vertical stacked blocks (display: block) "
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
        )
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
