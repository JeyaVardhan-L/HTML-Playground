# Web Application Frameworks (WAF) — Lab Assignment 3
## Core JavaScript Practicals & Beginner Learning Guide

**Subject:** Web Application Frameworks (WAF) Lab  
**Assignment:** Lab Assignment 3 — JavaScript Foundations, DOM, Events, Objects, and DHTML  
**Technologies:** Pure HTML5, CSS3, Vanilla JavaScript (Zero External Dependencies)  

---

## 1. Assignment Overview & Purpose

**Assignment 3** demonstrates the fundamental building blocks of **JavaScript on the client side**. 

Instead of an overengineered multi-page web application, this assignment delivers **four self-contained, beginner-friendly practicals** designed specifically for lab evaluation and demonstration. Every practical runs independently in any modern browser without needing Node.js, npm, backend servers, or internet access.

### Topics Covered
Every required topic from the lab syllabus is implemented and demonstrated:
1. **Functions** (Parameters, return values, invocation)
2. **Data Types** (String, Number, Boolean, Undefined, Null)
3. **Expressions** (Arithmetic, comparison, logical)
4. **Control Statements** (`if/else if/else`, `for` loop)
5. **DOM Methods & Objects** (`getElementById`, `querySelector`, `textContent`, `style`, `innerHTML`)
6. **Events & Event Listeners** (`submit`, `reset`, `click`, `dragstart`, `dragover`, `drop`)
7. **JavaScript Objects** (Object literals, properties, methods, `this` keyword)
8. **DHTML (Dynamic HTML)** (Dynamically altering styles, coordinates, and z-index based on user action)
9. **Error Handling** (`try`, `throw`, `catch`, `finally`)
10. **Built-in Objects & Methods** (`new Date()`, string methods like `.toUpperCase()`, `.toLowerCase()`, `.trim()`, `.includes()`)

---

## 2. Directory Structure

```text
Assignment-3/
├── README.md                      ← Assignment overview, execution guide & demonstration checklist
├── assets/
│   └── star.svg                   ← Local vector icon for Practical 3 (zero external dependencies)
├── practical-1-form.html          ← Practical 1: Student Registration Form with Validation
├── practical-2-basics.html        ← Practical 2: Core JS Basics, Data Types, Objects & Error Handling
├── practical-3-drag-drop.html     ← Practical 3: Drag-and-Drop Image with HTML5 Events & DHTML
├── practical-4-stacking.html      ← Practical 4: Dynamic Element Stacking using CSS z-index
└── docs/
    └── learning/
        ├── START-HERE.md          ← Orientation, learning roadmap, and architecture flow diagram
        ├── CODE-EXPLANATION.md    ← Line-by-line code explanation & interaction traces
        ├── JAVASCRIPT-FROM-ZERO.md← Theory guide explaining JS concepts in beginner-friendly language
        ├── VIVA-PREP.md           ← 22 high-yield lab exam questions with concise model answers
        ├── HANDS-ON-EXERCISES.md  ← 8 small modifications with hints and verification criteria
        └── GLOSSARY.md            ← Quick-reference dictionary of JavaScript and DOM terms
```

---

## 3. The Four Practicals at a Glance

| Practical | File | Key Demonstration | Syllabus Topics Covered |
| :--- | :--- | :--- | :--- |
| **Practical 1** | `practical-1-form.html` | Student registration form with client-side field validation, instant error messages, and dynamic summary box. | Functions, Form Validation, `if/else`, DOM Selection, `submit`/`reset` Events, `event.preventDefault()`. |
| **Practical 2** | `practical-2-basics.html` | Interactive laboratory demonstrating core language foundations, arithmetic expressions, objects, dates, string methods, and `try/catch`. | Primitive Data Types, Operators, Functions with Return Values, Loops, Objects, Date, String Methods, Error Handling. |
| **Practical 3** | `practical-3-drag-drop.html` | Interactive bordered canvas allowing user to drag a local SVG badge freely or into target zones, with live event logging. | HTML5 Drag & Drop Events (`dragstart`, `dragover`, `drop`), DOM manipulation, DHTML Coordinates. |
| **Practical 4** | `practical-4-stacking.html` | Three overlapping colored cards where clicking any card brings it dynamically to the front using CSS `z-index`. | `z-index`, Event Listeners, Counters, Positioning, DHTML Style Modification. |

---

## 4. How to Run the Practicals

Because each practical is completely self-contained, you have two simple ways to run them:

### Method A: Direct Browser Opening (No Server Needed)
1. Navigate to the `Assignment-3/` folder in your file explorer.
2. Double-click any of the four HTML files (e.g. `practical-1-form.html`).
3. The file will open directly in Google Chrome, Edge, Firefox, or Safari using the `file:///` protocol.

### Method B: Using Python Local Server
If your faculty prefers running through a local development server:
```powershell
# Navigate to the HTML-Playground root
cd c:\Users\user\Downloads\HTML-Playground\HTML-Playground

# Start Python's built-in web server on port 8000
python -m http.server 8000
```
Open your browser and visit:
- Practical 1: `http://localhost:8000/Assignment-3/practical-1-form.html`
- Practical 2: `http://localhost:8000/Assignment-3/practical-2-basics.html`
- Practical 3: `http://localhost:8000/Assignment-3/practical-3-drag-drop.html`
- Practical 4: `http://localhost:8000/Assignment-3/practical-4-stacking.html`

---

## 5. Topic-to-Practical Mapping Matrix

| Syllabus Requirement | Where Implemented | Code Identifier / Evidence |
| :--- | :--- | :--- |
| **Functions** | `practical-1-form.html`<br>`practical-2-basics.html` | `setError()`, `clearAllErrors()`, `calculateCircleArea(radius)`, `getGrade(score)`, `divideNumbers(x, y)` |
| **Data Types** | `practical-2-basics.html`<br>`practical-1-form.html` | `typesData` table verifying `typeof` for String, Number, Boolean, Undefined, Null; Number conversion `Number(ageValue)` |
| **Expressions** | `practical-2-basics.html`<br>`practical-1-form.html` | Arithmetic (`+`, `-`, `*`, `/`, `%`), comparison (`===`, `>`, `<`), and logical (`&&`, `!`) |
| **Control Statements** | `practical-1-form.html`<br>`practical-2-basics.html` | `if (fullName === "") ... else if`, `getGrade(score)`, `for (let i = 1; i <= 5; i++)` |
| **DOM Methods & Objects** | All Practicals | `document.getElementById()`, `document.querySelector()`, `document.querySelectorAll()`, `element.textContent`, `element.innerHTML`, `element.style` |
| **Events & Event Listeners** | All Practicals | `addEventListener("submit", ...)`, `"click"`, `"dragstart"`, `"dragover"`, `"drop"`, `"reset"` |
| **JavaScript Objects** | `practical-2-basics.html` | Object literal `student` with properties (`name`, `rollNo`, `marks`) and method `calculateAverage()` using `this` |
| **DHTML (Dynamic HTML)** | `practical-3-drag-drop.html`<br>`practical-4-stacking.html` | Dynamically changing coordinates (`style.left`, `style.top`), opacity, and stacking order (`style.zIndex`) upon user actions |
| **Error Handling** | `practical-2-basics.html` | `try { ... } catch (err) { ... } finally { ... }` with custom `throw new Error(...)` |
| **Built-in Objects** | `practical-2-basics.html`<br>`practical-3-drag-drop.html` | `new Date().toDateString()`, `.toLocaleTimeString()`, `Math.PI`, `Math.round()`, string `.trim()`, `.toUpperCase()` |

---

## 6. Demonstration Checklist for Lab Evaluation

Before showing your work to the instructor, run through this quick 2-minute checklist:

- [ ] **Practical 1 (Form):**
  - Click "Register" with blank fields → Verify 7 red error messages appear.
  - Fill invalid data (Age: 12, Phone: 12345, Password: abc) → Verify specific validation messages appear.
  - Enter valid data → Verify green success box appears with neatly formatted details.
  - Click "Reset" → Verify inputs and success message clear.
- [ ] **Practical 2 (Basics):**
  - Verify the data types table renders with correct `typeof` results.
  - Change radius to `7` and click "Calculate Circle Area" → Verify `153.94` displays.
  - Change score to `92` and click "Evaluate Grade" → Verify `Grade A` displays.
  - Change divisor to `0` and click "Perform Division" → Verify the red `ZeroDivisionError` is caught gracefully without breaking the page.
- [ ] **Practical 3 (Drag & Drop):**
  - Click and drag the star badge across the canvas → Verify the live event log records `dragstart`, `dragover`, and `drop`.
  - Drop the star inside "Target Zone A" or "Target Zone B" → Verify it snaps into the center.
  - Click "Reset Image Position" → Verify it returns to `(50px, 50px)`.
- [ ] **Practical 4 (Stacking):**
  - Click Box 1 (Red) → Verify it moves in front of Box 2 and Box 3.
  - Click Box 2 (Blue) → Verify it moves to the very top.
  - Check the live status pills → Verify `z-index` increments smoothly.
  - Click "Reset Layers" → Verify Box 3 returns to the top.

---

## 7. Learning Documentation

Start your review with the comprehensive guides in [`docs/learning/`](docs/learning/):

1. [**`START-HERE.md`**](docs/learning/START-HERE.md) — Big picture orientation and learning sequence.
2. [**`CODE-EXPLANATION.md`**](docs/learning/CODE-EXPLANATION.md) — Step-by-step tour and execution traces.
3. [**`JAVASCRIPT-FROM-ZERO.md`**](docs/learning/JAVASCRIPT-FROM-ZERO.md) — Plain-English guide to JavaScript syntax and theory.
4. [**`VIVA-PREP.md`**](docs/learning/VIVA-PREP.md) — 22 viva examination questions with model answers.
5. [**`HANDS-ON-EXERCISES.md`**](docs/learning/HANDS-ON-EXERCISES.md) — 8 beginner coding exercises with hints and answers.
6. [**`GLOSSARY.md`**](docs/learning/GLOSSARY.md) — Terminology cheat sheet.
