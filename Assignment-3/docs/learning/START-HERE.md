# Start Here: Assignment 3 Learning Roadmap

Welcome to the beginner's learning guide for **Web Application Frameworks (WAF) Lab Assignment 3**!

If you are new to JavaScript or feel unsure how HTML, CSS, DOM methods, and events connect together, this guide is designed specifically for you.

---

## 1. What This Assignment Demonstrates

In **Assignment 2**, we focused heavily on **HTML structure** (iframes, semantic tags, tables) and **CSS presentation** (the box model, CSS Grid, media queries).

In **Assignment 3**, we bring our web pages to life with **JavaScript**. JavaScript is the programming language of the web that adds **logic, computation, event handling, and dynamic updates (DHTML)** to static HTML elements.

Across four independent, beginner-friendly practicals, this assignment covers:
- **Core Language**: Variables (`let`/`const`), Primitive Data Types, Arithmetic/Comparison Expressions, Functions with Return Values, `if/else` Decisions, and `for` Loops.
- **Data Structures & Built-ins**: Object Literals, Methods using `this`, the `Date` Object, and Common String Methods.
- **Browser Interaction**: DOM selection (`getElementById`, `querySelector`), DOM manipulation (`textContent`, `style`, `innerHTML`), and Error Handling (`try/catch/finally`).
- **Events & DHTML**: Handling user clicks, form submissions, and HTML5 drag-and-drop events to dynamically change coordinates and stacking order (`z-index`).

---

## 2. Mental Model: How HTML, CSS, JavaScript, and Events Work Together

Understanding how the browser processes your code is the secret to feeling confident during a lab viva:

```text
+-----------------------------------------------------------------------------------------+
|                                    WEB BROWSER                                          |
|                                                                                         |
|  1. HTML (The Skeleton)                                                                 |
|     <input id="age">                                                                    |
|     <button id="btn">Submit</button>                                                    |
|            |                                                                            |
|            v                                                                            |
|  2. DOM Tree (Document Object Model)                                                    |
|     The browser parses HTML tags into a live in-memory tree of JS objects:              |
|     document.getElementById("age")                                                      |
|            ^                                                                            |
|            | reads / modifies properties (.value, .textContent)                         |
|            |                                                                            |
|  3. JAVASCRIPT (The Brain & Wiring)                                                     |
|     function validateAge() {                                                            |
|       const val = document.getElementById("age").value;                                |
|       if (val < 18) { ... }                                                             |
|     }                                                                                   |
|            ^                                                                            |
|            | executes in response to                                                    |
|            |                                                                            |
|  4. BROWSER EVENTS (Sensors)                                                            |
|     User clicks, types, or drags --> fires "click", "submit", "dragstart"               |
|     addEventListener("click", validateAge);                                             |
|            |                                                                            |
|            v                                                                            |
|  5. DHTML (Dynamic HTML Style Updates)                                                  |
|     element.style.color = "red";                                                        |
|     element.style.zIndex = 10;                                                          |
|     CSS re-renders the element visually on the screen without reloading!                |
+-----------------------------------------------------------------------------------------+
```

### The Difference in One Sentence:
- **HTML** gives the page its structure and content.
- **CSS** gives the page its colors, layout, and visual styling.
- **JavaScript** provides the logic that reacts to user events and updates the HTML/CSS on the fly.

---

## 3. What Each Practical Does

| File | What It Does | Key Topic |
| :--- | :--- | :--- |
| **`practical-1-form.html`** | A student registration form that validates 7 fields (Name, Age, Email, Phone, Address, Password, Gender) on submit, displays error messages beside fields, and renders a summary box when all pass. | Form Validation, `submit` event, `event.preventDefault()`, `if/else`, DOM manipulation. |
| **`practical-2-basics.html`** | An interactive laboratory with 8 distinct panels demonstrating JavaScript primitives, expressions, circle area function, grade calculator, loops, objects, dates, string methods, and `try/catch`. | Language foundations, Functions, Objects, Loops, Error Handling. |
| **`practical-3-drag-drop.html`** | An interactive bordered canvas containing a local SVG star badge that users can drag freely or drop into Target Zones A and B, complete with a real-time event log. | HTML5 Drag & Drop (`dragstart`, `dragover`, `drop`), coordinates, DHTML. |
| **`practical-4-stacking.html`** | Three overlapping colored cards (Red, Blue, Green). Clicking any card brings it dynamically to the front using CSS `z-index` and a JavaScript counter. | CSS `z-index`, `click` event listener, DHTML style modification. |

---

## 4. Which File to Open First & Recommended Learning Order

Follow this sequence to build your knowledge naturally:

```text
Step 1: Open practical-2-basics.html in your browser
        (See how primitive types, variables, expressions, and functions work)
           |
           v
Step 2: Open practical-1-form.html in your browser
        (See how functions, conditions, and DOM events validate real user input)
           |
           v
Step 3: Open practical-4-stacking.html in your browser
        (Click the overlapping boxes to understand CSS z-index and click events)
           |
           v
Step 4: Open practical-3-drag-drop.html in your browser
        (Drag the star badge to master complex drag-and-drop events and DHTML)
```

### Recommended Reading Sequence for Documentation:
1. **`START-HERE.md`** *(You are here)*: Grasp the big picture and architecture.
2. **`JAVASCRIPT-FROM-ZERO.md`**: Read the fundamental concepts explained in simple language.
3. **`CODE-EXPLANATION.md`**: Walk through every line of code in each of the 4 practicals.
4. **`HANDS-ON-EXERCISES.md`**: Try 8 small modifications to prove your understanding.
5. **`VIVA-PREP.md`**: Practice speaking 22 high-yield lab exam questions.
6. **`GLOSSARY.md`**: Keep handy as a technical cheat sheet.

---

## 5. How to Run Each Practical

All files are completely self-contained with embedded styles and scripts.

### Option 1 (Easiest): Double Click
Go to `Assignment-3/` in Windows File Explorer and double-click:
- `practical-1-form.html`
- `practical-2-basics.html`
- `practical-3-drag-drop.html`
- `practical-4-stacking.html`

### Option 2: Local Python Server
Run in PowerShell:
```powershell
cd c:\Users\user\Downloads\HTML-Playground\HTML-Playground
python -m http.server 8000
```
Open your browser and navigate to `http://localhost:8000/Assignment-3/practical-1-form.html`.

Let's begin with the language foundations in [JAVASCRIPT-FROM-ZERO.md](JAVASCRIPT-FROM-ZERO.md)!
