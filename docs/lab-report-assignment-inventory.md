# WAF Lab Report Assignment Inventory & Capability Matrix

**Repository:** `HTML-Playground`  
**Date of Audit:** October 27, 2026  
**Auditor:** Automated Lab Report System Audit  

---

## Executive Summary

An audit of the `HTML-Playground` repository was conducted to inventory all coursework deliverables for the Web Application Frameworks (WAF) Lab. The repository contains coursework spanning pure static HTML5/CSS/JavaScript interfaces, component-based React applications, Express.js backend servers, and MongoDB aggregation and query practicals.

This document establishes the verified inventory for **Assignments 1 through 7**, identifying actual objectives, source files, dependencies, runtime requirements, server processes, routes, evidence types, and known vs. unknown parameters strictly based on repository evidence.

---

## Assignment 1: MVC Architecture Implementation

- **Directory:** `MVC_L1/`
- **Formal Title:** Lab Assignment 1: MVC Architecture Implementation (Verified via `MVC_L1/Documentation.html`)
- **Academic Aim / Objective:**
  To build a web application from scratch using Node.js, Express, and EJS that successfully implements the Model-View-Controller (MVC) architectural pattern, separating data handling, routing/control logic, and presentation markup.
- **Tech Stack & Dependencies:**
  - Runtime: Node.js (CommonJS)
  - Framework: Express.js (`express` v4)
  - View Engine: EJS (`ejs` v3)
  - Dependencies: Installed and verified in `MVC_L1/node_modules/`
- **Architecture & Key Files:**
  - Model: `models/messageModel.js` — exports `getMessage()` returning `"Hello from the Model!"`.
  - Controller: `controllers/messageController.js` — exports `showMessage(req, res)` invoking `getMessage()` and rendering `view.ejs` with `{ message: data }`.
  - View: `views/view.ejs` — HTML5 template rendering `<h1>MVC Architecture Lab</h1>` and `<h2><%= message %></h2>`.
  - Entry Point: `app.js` — configures EJS view engine, mounts `GET /` to `showMessage`, and listens on port 3000.
  - Manifest: `package.json` with `"start": "node app.js"`.
  - Documentation: `Documentation.html` with full implementation explanation and printable layout.
- **Execution & Server Requirements:**
  - Command: `node app.js` in `MVC_L1/`
  - Default Port: 3000 (currently hardcoded in `app.js`, can accept `process.env.PORT || 3000`)
  - Server Readiness URL: `http://localhost:3000/` (returns HTTP 200 with HTML)
- **Source Files for Appendix:**
  1. `app.js` (Server & Route Setup)
  2. `controllers/messageController.js` (Controller Logic)
  3. `models/messageModel.js` (Model Data Store)
  4. `views/view.ejs` (EJS Presentation Template)
  5. `package.json` (Project Manifest)
- **Required Evidence:**
  1. Browser rendering of `http://localhost:3000/` displaying "MVC Architecture Lab" and "Hello from the Model!".
  2. Terminal server start log (`Server is running on http://localhost:3000`).
  3. MVC directory separation and code integrity.

> **Note on Unnumbered `Assignment/` Directory:**
> The repository also contains an unnumbered folder `Assignment/` with three subdirectories (`backend/` for RESTful Book API, `frontend/` for React Hooks/Props/Context, and `middleware-demo/` for Express middleware chain). Its README labels it "Web Application Framework — Assignment". In contrast, `MVC_L1/Documentation.html` explicitly states "Lab Assignment 1: MVC Architecture Implementation". Both are documented; `MVC_L1` represents Assignment 1.

---

## Assignment 2: Minimalist Grayscale Interface (Frontier AI Atlas)

- **Directory:** `Assignment-2/`
- **Formal Title:** Lab Assignment 2: Minimalist Grayscale Interface (Mac-Inspired UI) — Frontier AI Atlas
- **Academic Aim / Objective:**
  To design, develop, and verify an educational multi-page web application ("Frontier AI Atlas") utilizing HTML5 semantic tags, inline frame (`<iframe name='content'>`) routing, a developer survey form constructed strictly within a tabular layout (`<table class='form-table'>`), client-side JavaScript validation, external and standalone hyperlinks, responsive design principles, and a clean Apple-inspired grayscale CSS design system.
- **Tech Stack & Dependencies:**
  - Pure HTML5, CSS3 (Custom Properties, Flexbox, Grid), Vanilla JavaScript (ES2022)
  - Zero external dependencies or build tools
- **Architecture & Key Files:**
  - Navigation Shell: `index.html` (Header, Nav, `<iframe name="content">`, Footer)
  - Subpages: `home.html`, `models.html`, `survey.html`, `articles.html`
  - Styling: `css/style.css` (Grayscale CSS tokens, responsive breakpoints, tabular form layout)
  - Scripting: `js/script.js` (PostMessage iframe height auto-resizer, client-side validation, standalone page detection)
- **Execution & Server Requirements:**
  - Command: Python built-in `http.server` serving `Assignment-2/`
  - Default Port: 8000
  - Server Readiness URL: `http://localhost:8000/index.html`
- **Source Files for Appendix:**
  1. `index.html` (Main Frame Shell & Navigation)
  2. `home.html` (Overview & Architecture)
  3. `models.html` (Foundation Model Comparison)
  4. `survey.html` (Tabular Form & Client-Side Validation)
  5. `articles.html` (Semantic Technical Guides)
  6. `css/style.css` (Minimalist Grayscale Stylesheet)
  7. `js/script.js` (Client-Side Logic & PostMessage Bridge)
- **Required Evidence:**
  - 9 automated Playwright scenes: Primary Interface, Subpage Navigation, Tabular Form Layout, Validation Errors, Form Submission Feedback, Semantic Articles, Foundation Model Grid, Mobile Viewport (390x844), and Standalone Detection Banner.

---

## Assignment 3: JavaScript Foundations, DOM, Events, Objects & DHTML

- **Directory:** `Assignment-3/`
- **Formal Title:** Lab Assignment 3 — JavaScript Foundations, DOM, Events, Objects, and DHTML
- **Academic Aim / Objective:**
  To demonstrate fundamental client-side JavaScript mechanisms across four self-contained, beginner-friendly practicals:
  1. Student Registration Form with field validation, dynamic error alerts, and submission summary.
  2. Core JavaScript foundations: primitive data types, operators, loops, custom object literals, `Date` methods, string methods, and `try/catch/finally` error handling.
  3. HTML5 Drag-and-Drop events (`dragstart`, `dragover`, `drop`) with local SVG element manipulation and live event logging.
  4. Dynamic element stacking utilizing CSS `z-index` and interactive layer manipulation controls.
- **Tech Stack & Dependencies:**
  - Pure HTML5, CSS3, Vanilla JavaScript
  - Local vector assets: `assets/star.svg`
  - Zero external dependencies, npm packages, or build tools
- **Architecture & Key Files:**
  - `practical-1-form.html` — Form validation (`submit`/`reset` events, regex, `event.preventDefault()`, dynamic summary).
  - `practical-2-basics.html` — Data types, arithmetic/logical expressions, objects, Date, String methods, exception handling.
  - `practical-3-drag-drop.html` — HTML5 drag-and-drop canvas, target drop zones, dynamic coordinates, live event log.
  - `practical-4-stacking.html` — 3 overlapping colored cards, interactive z-index manipulation, layer order readouts.
  - Comprehensive documentation in `docs/learning/`.
- **Execution & Server Requirements:**
  - Command: Python built-in `http.server` serving `Assignment-3/`
  - Default Port: 8000
  - Readiness URLs: `/practical-1-form.html`, `/practical-2-basics.html`, `/practical-3-drag-drop.html`, `/practical-4-stacking.html`
- **Source Files for Appendix:**
  1. `practical-1-form.html` (Form Validation Practical)
  2. `practical-2-basics.html` (Core JS Foundations & Objects)
  3. `practical-3-drag-drop.html` (Drag & Drop Events Practical)
  4. `practical-4-stacking.html` (Dynamic Stacking & z-index Practical)
- **Required Evidence:**
  - Form validation with error states and successful submission summary.
  - Core JS interactive calculators and object method evaluations.
  - Drag-and-drop target zone interaction and event log entries.
  - Layer reordering with updated `z-index` values.

---

## Assignment 4: Express Server with Browser Fetch & Core React Practicals

- **Directory:** `Assignment-4/`
- **Formal Title:** Lab Assignment 4 — Express Server with Browser Fetch & Core React Practicals
- **Academic Aim / Objective:**
  To master modern client-server communication and component architecture across two integrated sub-projects:
  1. Server-Side Express & Browser Fetch (`express-fetch/`): Node.js + Express backend serving static HTML and providing an asynchronous `GET /api/student` JSON endpoint, consumed via native `fetch()` with async/await.
  2. Component-Based React Architecture (`react-practicals/`): React 18 + Vite practical laboratory implementing five distinct components demonstrating State (`useState`), Class Components (`extends React.Component`), Props (parent-to-child data flow), Three React Hooks (`useState`, `useRef`, `useEffect`), and Function Components.
- **Tech Stack & Dependencies:**
  - `express-fetch/`: Node.js, Express.js (`express` v4) — verified in `express-fetch/node_modules/`
  - `react-practicals/`: React 18 (`react`, `react-dom`), Vite 6 (`vite`, `@vitejs/plugin-react`) — verified in `react-practicals/node_modules/` and pre-built in `react-practicals/dist/`
- **Architecture & Key Files:**
  - `express-fetch/server.js`: Express server with static middleware, terminal logging, and `GET /api/student`.
  - `express-fetch/public/index.html`: Client interface with "Fetch Student Data" button and asynchronous DOM injection.
  - `react-practicals/src/App.jsx`: Main tabbed container housing all practicals.
  - `react-practicals/src/components/StateCounter.jsx` (Practical 2: React State).
  - `react-practicals/src/components/ClassStudent.jsx` (Practical 3: Class Component).
  - `react-practicals/src/components/StudentProps.jsx` (Practical 4: React Props).
  - `react-practicals/src/components/HooksDemo.jsx` (Practical 5: Three Hooks).
  - `react-practicals/src/components/FunctionStudent.jsx` (Practical 6: Function Component).
  - `react-practicals/src/styles.css`: Clean college-practical styles.
- **Execution & Server Requirements:**
  - Sub-project 1 (`express-fetch`): `node server.js` inside `Assignment-4/express-fetch` (Default port: 3000 or custom port).
  - Sub-project 2 (`react-practicals`): Static serving of pre-built `dist/` or `npx vite preview` / `npm run dev`.
- **Source Files for Appendix:**
  1. `express-fetch/server.js` (Express Server & API Endpoint)
  2. `express-fetch/public/index.html` (Fetch Client Interface)
  3. `react-practicals/src/App.jsx` (React Tabbed Container)
  4. `react-practicals/src/components/StateCounter.jsx` (State Practical)
  5. `react-practicals/src/components/ClassStudent.jsx` (Class Component Practical)
  6. `react-practicals/src/components/StudentProps.jsx` (Props Practical)
  7. `react-practicals/src/components/HooksDemo.jsx` (Three Hooks Practical)
  8. `react-practicals/src/components/FunctionStudent.jsx` (Function Component Practical)
  9. `react-practicals/src/styles.css` (Component Stylesheet)
- **Required Evidence:**
  - Express server responding to `GET /api/student` and browser DOM update.
  - React tabbed interface showing active state counter, class component render, props list mapping, hooks timer/ref demo, and functional component.

---

## Assignment 5: Fetching Data with a New Connection Using Express.js

- **Directory:** `Assignment-5/`
- **Formal Title:** Lab Assignment 5 — Fetching the Data with a New Connection Using Express.js
- **Academic Aim / Objective:**
  To demonstrate asynchronous, decoupled web architecture where client requests open brand new HTTP connections on demand without reloading the host page. The Express server maintains a server-side request counter, logs each incoming request to the terminal in a numbered format, timestamps responses, and transmits dynamic JSON to the browser fetch client.
- **Tech Stack & Dependencies:**
  - Node.js runtime
  - Express.js (v4) — verified in `Assignment-5/node_modules/`
  - Browser Fetch API (`async` / `await`)
  - Vanilla HTML5 and CSS3
- **Architecture & Key Files:**
  - `server.js`: Express server configured on port 3001, maintaining `requestCount`, serving static assets from `public/`, and exposing `GET /api/student`. Includes port conflict detection (`EADDRINUSE`).
  - `public/index.html`: College lab design with `#fetchBtn`, loading indicators, and dynamic student card displaying student details, request sequence number (`#1`, `#2`, ...), and server timestamp.
  - Documentation in `docs/learning/`.
- **Execution & Server Requirements:**
  - Command: `node server.js` in `Assignment-5/`
  - Default Port: 3001
  - Readiness URL: `http://localhost:3001/`
  - API Endpoint: `http://localhost:3001/api/student`
- **Source Files for Appendix:**
  1. `server.js` (Express Server with Request Counter & Timestamping)
  2. `public/index.html` (Browser Client UI & Async Fetch Handler)
  3. `package.json` (Project Configuration)
- **Required Evidence:**
  - Browser UI showing initial idle state.
  - Browser UI after clicking "Fetch Student Data" showing request number `#1` with server timestamp.
  - Repeated fetch showing incremented request count (e.g. `#2`) proving new HTTP connection creation.
  - Server terminal log confirming `GET /api/student: request N`.

---

## Assignment 6: MongoDB Lookup, Aggregation Pipelines & Express REST API

- **Directory:** `Assignment-6/`
- **Formal Title:** Lab Assignment 6 — MongoDB, Aggregation Pipelines & Express REST API
- **Academic Aim / Objective:**
  To implement advanced database aggregations and RESTful web services in Node.js using the official native MongoDB driver (`mongodb` v6), without ORM/ODM abstraction:
  1. Relational NoSQL join (`$lookup` and `$unwind`) between students and departments collections.
  2. Full CRUD Express REST API (`GET`, `POST`, `PUT`, `DELETE` on `/students`) with validation and unique index enforcement on `rollNo`.
  3. Nested array processing (`$unwind`) and grouping (`$group`) to compute subject totals and averages per student.
  4. Filtered grouping (`$match` followed by `$group`) to count students scoring > 60 by branch.
  5. Multi-accumulator aggregation computing branch-wise average, maximum, and minimum marks sorted descending.
- **Tech Stack & Dependencies:**
  - Runtime: Node.js (ES2022)
  - Driver: Official MongoDB Node.js Driver (`mongodb` v6.12.0)
  - Framework: Express.js (`express` v4)
  - Database: MongoDB running locally on port 27017, database name `waf_assignment_6`
  - Dependencies: Verified in `Assignment-6/node_modules/`
- **Architecture & Key Files:**
  - `scripts/seed.js` — Idempotent database seeder creating 3 departments and 8 students with deterministic ObjectIds.
  - `api/server.js` — Express REST API on Port 3002 handling full student lifecycle.
  - `scripts/lookup-students.js` — Req 1: `$lookup` department join.
  - `scripts/subject-summary.js` — Req 3: `$unwind` and `$group` subject analysis.
  - `scripts/branch-above-60.js` — Req 4: `$match` and `$group` scoring filter.
  - `scripts/branch-statistics.js` — Req 5: Branch statistics (`$avg`, `$max`, `$min`) sorted desc.
- **Execution & Server Requirements:**
  - Database: MongoDB service active on `127.0.0.1:27017`
  - Seeding: `node scripts/seed.js`
  - API Server: `node api/server.js` (Default port: 3002)
  - Scripts: Executable standalone via Node.js
- **Source Files for Appendix:**
  1. `api/server.js` (Express REST API with MongoDB Native Driver)
  2. `scripts/seed.js` (Database Seeder with Unique Indexes)
  3. `scripts/lookup-students.js` (Requirement 1: $lookup Join)
  4. `scripts/subject-summary.js` (Requirement 3: $unwind & $group Subjects)
  5. `scripts/branch-above-60.js` (Requirement 4: $match & $group Branch Filter)
  6. `scripts/branch-statistics.js` (Requirement 5: Branch Statistics Aggregation)
  7. `package.json` (Project Manifest)
- **Required Evidence:**
  - Database seed execution and connection confirmation.
  - Aggregation pipeline script outputs (lookup, subject summary, branch filter, statistics).
  - Express REST API live request responses (`GET /`, `GET /students`, `POST /students`, `GET /students/:rollNo`).

---

## Assignment 7: MongoDB Queries, Cursor Chaining, Regex & Atomic Updates

- **Directory:** `Assignment-7/`
- **Formal Title:** Lab Assignment 7 — MongoDB Queries, Cursor Chaining, Regex & Atomic Updates
- **Academic Aim / Objective:**
  To explore foundational MongoDB queries, cursor methods, data typing, and concurrency patterns in Node.js:
  1. Cursor chaining with `sort({ marks: -1 })` and `limit(3)` to determine top scorers with deterministic tie-breaking.
  2. BSON primary key lookups resolving 12-byte `new ObjectId("...")` instances.
  3. Safe destructive operations using `deleteMany({ marks: { $lt: 40 } })` with safeguard confirmations and recovery.
  4. Pattern matching with regular expressions (`$regex: "^M"` with case-insensitivity).
  5. Atomic inventory concurrency: Library book issue and return management using `findOneAndUpdate` with atomic `$inc` operators and guard conditions (`{ copies: { $gt: 0 } }`) to prevent negative inventory under race conditions.
- **Tech Stack & Dependencies:**
  - Runtime: Node.js (ES2022)
  - Driver: Official MongoDB Node.js Driver (`mongodb` v6)
  - Database: MongoDB running locally on port 27017, database name `waf_assignment_7`
  - Dependencies: Verified in `Assignment-7/node_modules/`
- **Architecture & Key Files:**
  - `scripts/seed.js` — Idempotent seeder populating departments, students, and library books.
  - `scripts/top-three.js` — Req 6: Top 3 scorers cursor pipeline.
  - `scripts/find-by-id.js` — Req 7: BSON ObjectId lookup.
  - `scripts/delete-below-40.js` — Req 8: Safe deletion below 40 marks.
  - `scripts/names-starting-m.js` — Req 9: Regex pattern matching on names.
  - `scripts/library-management.js` — Req 10: Atomic book issue and return operations.
- **Execution & Server Requirements:**
  - Database: MongoDB service active on `127.0.0.1:27017`
  - Seeding: `node scripts/seed.js`
  - Scripts: Executable standalone via Node.js
- **Source Files for Appendix:**
  1. `scripts/seed.js` (Database Seeder for Departments, Students, and Books)
  2. `scripts/top-three.js` (Requirement 6: Cursor sort and limit)
  3. `scripts/find-by-id.js` (Requirement 7: BSON ObjectId Query)
  4. `scripts/delete-below-40.js` (Requirement 8: Filtered deleteMany)
  5. `scripts/names-starting-m.js` (Requirement 9: Case-Insensitive $regex)
  6. `scripts/library-management.js` (Requirement 10: Atomic Concurrency & Library System)
  7. `package.json` (Project Manifest)
- **Required Evidence:**
  - Seed execution populating `waf_assignment_7`.
  - Top three students cursor query execution output.
  - Document retrieval by BSON ObjectId.
  - Deletion of records below 40 marks and count confirmation.
  - Names matching regex pattern `^M`.
  - Library issue/return atomic operation verification.

---

## Cross-Assignment Execution & Evidence Strategy Matrix

| Assignment | Primary Type | Server / Execution Command | Default Port | Evidence Capture Strategy |
| :--- | :--- | :--- | :--- | :--- |
| **Assignment 1** | Express MVC (EJS) | `node app.js` in `MVC_L1/` | 3000 | Browser screenshot of `/` + terminal startup |
| **Assignment 2** | Static HTML5 / CSS / JS | Python `http.server` in `Assignment-2/` | 8000 | 9 Playwright scenes (desktop, mobile, form, iframe) |
| **Assignment 3** | Static HTML5 / CSS / JS | Python `http.server` in `Assignment-3/` | 8000 | 4 Playwright scenes (form validation, basics, drag-drop, stacking) |
| **Assignment 4** | Express API + React 18 | `node server.js` in `Assignment-4/express-fetch` + React static/dev | 3000 & 5173 | Playwright scenes for Express fetch client & React tabbed components |
| **Assignment 5** | Express Fetch Counter | `node server.js` in `Assignment-5/` | 3001 | Playwright scenes capturing initial state & dynamic fetch counter increments |
| **Assignment 6** | MongoDB & Express API | `node api/server.js` in `Assignment-6/` + Node script runners | 3002 | API request evidence (`GET /`, `GET /students`) + script aggregation outputs |
| **Assignment 7** | MongoDB Queries & Scripts| Node script runners in `Assignment-7/scripts/` | N/A (CLI) | Real command executions capturing query outputs & atomic library updates |

---

## Known vs. Unknown Parameters

- **Known & Verified:**
  - Repository structure, directory layouts, and source file locations for all seven assignments.
  - Actual student identity in coursework files: "Jey" / Roll No: "9057" / GITAM Deemed to be University, Department of Computer Science & Engineering.
  - Local runtime tools: Node.js, Python 3.14 (with Playwright, python-docx, Pillow, pypdfium2), Microsoft Word 16.0 COM automation.
  - Live MongoDB instance running locally at `127.0.0.1:27017`.
- **Unknown / Unassumed:**
  - Official institution submission dates (dynamically populated with current date or configured string).
  - External network API credentials (all practicals use self-contained in-memory or local MongoDB databases; no remote cloud APIs required).
