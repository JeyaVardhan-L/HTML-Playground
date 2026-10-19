# Project Glossary: Key Terms Explained

A quick-reference dictionary of technical web terms used in the **Frontier AI Atlas** codebase. Each term is explained in 1–2 plain sentences with code examples.

---

## 1. HTML Terms

### Attribute
Additional information or settings placed inside an HTML opening tag, formatted as `name="value"`.  
*Example*: `id="content-frame"` or `class="nav-link"`.

### Boilerplate
The standard minimal HTML structure required on every web page before adding custom content.  
*Example*: `<!DOCTYPE html>`, `<html>`, `<head>`, and `<body>`.

### Block Element
An element that starts on a new line and spans the full available width of its container.  
*Example*: `<div>`, `<p>`, `<h1>`, and `<header>`.

### Inline Element
An element that only takes up as much width as its content and does not force a line break.  
*Example*: `<span>`, `<a>`, and `<strong>`.

### Semantic Element
An HTML5 tag whose name clearly communicates its structural purpose and content to developers and browsers.  
*Example*: `<nav>`, `<article>`, `<section>`, `<main>`, and `<footer>`.

### Void (Self-Closing) Element
An HTML element that cannot contain nested elements or text and therefore does not require a closing tag.  
*Example*: `<input>`, `<meta>`, and `<link>`.

### `<iframe>` (Inline Frame)
An HTML5 container that embeds another independent HTML document inside the current page.  
*Example*: `<iframe src="home.html" name="content"></iframe>`.

### `target` Attribute
An attribute on anchor tags (`<a>`) indicating where the linked resource should open.  
*Example*: `target="content"` opens inside our iframe; `target="_blank"` opens in a fresh browser tab.

### `scope` Attribute
An accessibility attribute placed on `<th>` cells to declare whether the header applies to a column or a row.  
*Example*: `<th scope="col">Model Family</th>`.

### `novalidate`
A boolean attribute on `<form>` that disables default browser validation popups so JavaScript can handle errors.  
*Example*: `<form id="aiSurveyForm" novalidate>`.

---

## 2. CSS Terms

### CSS Custom Property (Variable)
A user-defined property starting with `--` that stores a reusable value (like a color or radius) across a stylesheet.  
*Example*: `--background: #f5f5f7;` retrieved using `var(--background)`.

### The CSS Box Model
The foundational rule of web layout stating that every element is a rectangular box made of Content, Padding, Border, and Margin.  
*Example*: In `.model-card`, content is enclosed by `padding: 1.25rem;` and `border: 1px solid var(--border-light);`.

### `box-sizing: border-box`
A CSS setting that includes padding and borders inside an element's total width and height, preventing layout breakage.  
*Example*: `*, *::before, *::after { box-sizing: border-box; }`.

### Flexbox (`display: flex`)
A CSS layout mode designed for distributing space and aligning items along a single axis (either horizontal or vertical).  
*Example*: `.header-inner { display: flex; justify-content: space-between; }`.

### CSS Grid (`display: grid`)
A 2-dimensional CSS layout engine that structures elements across both rows and columns simultaneously.  
*Example*: `.cards-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); }`.

### Media Query
A CSS block that applies specific styling rules only when certain device conditions (like screen width) are met.  
*Example*: `@media (max-width: 768px) { ... }`.

### Pseudo-Class
A keyword added to a CSS selector that specifies a special state of the targeted element.  
*Example*: `:hover` (when mouse hovers), `:focus` (when input is selected), `:checked` (when radio/box is checked).

### System Font Stack
A font declaration that instructs the browser to use the operating system's built-in UI font rather than downloading external web fonts.  
*Example*: `-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif`.

---

## 3. JavaScript & DOM Terms

### DOM (Document Object Model)
The browser's in-memory, tree-structured representation of an HTML document that JavaScript can inspect and modify.  
*Example*: Using `document.getElementById("modelSearch")` to access the search box.

### Event
A signal emitted by the browser when an action occurs (like a click, keystroke, page load, or window resize).  
*Example*: `"click"`, `"input"`, `"submit"`, `"resize"`.

### Event Listener
A JavaScript method that registers a callback function to execute whenever a specified event is detected on an element.  
*Example*: `button.addEventListener("click", function() { ... })`.

### `querySelector` and `querySelectorAll`
DOM methods that search for elements using standard CSS selector syntax.  
*Example*: `document.querySelector('input[name="experience"]:checked')`.

### `event.preventDefault()`
A method that halts the browser's default reaction to an event (such as preventing a form from refreshing the page).  
*Example*: `e.preventDefault()` inside the `submit` handler.

### `window.self !== window.top`
A JavaScript check that tests whether the current window is running inside an iframe (`window.self`) or as the top window (`window.top`).  
*Example*: Used in `script.js` to determine whether to send height to the parent frame or show the standalone notice.

### Client-Side Validation
The process of inspecting user form inputs in the browser using JavaScript before submitting data to a server.  
*Example*: Checking `if (!email.includes("@"))` and alerting the user.

### Sanitization (Escaping)
Replacing raw HTML characters (like `<` and `&`) with safe HTML entities (`&lt;` and `&amp;`) to prevent malicious script injection.  
*Example*: The `escapeText()` function in `js/script.js`.
