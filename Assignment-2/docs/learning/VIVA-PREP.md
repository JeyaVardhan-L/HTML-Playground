# Lab Viva Preparation: 15 High-Yield Questions & Answers

This guide prepares you for your lab examination or viva voce. Every answer is tailored specifically to your **Frontier AI Atlas** implementation, phrased in clear, beginner-friendly language that you can comfortably speak to an examiner.

---

### Question 1: What is an `<iframe>` and how does it work in your project?
- **Model Answer**: An `<iframe>` (inline frame) is an HTML5 element that embeds another HTML document inside the current page. In my `index.html`, the iframe has `name="content"`. The top navigation links use `target="content"` to load different subpages (like `home.html` or `models.html`) directly inside that frame without reloading the parent header and footer.
- **Code Location**: `index.html` (lines 33–41)
- **Likely Follow-Up**: *Why not use `<frameset>` instead?*
  - **Answer**: `<frameset>` was deprecated and completely removed in HTML5. It broke browser bookmarking, was bad for search engines, and couldn't adapt to mobile screens. An `<iframe>` is modern and behaves like a normal responsive element inside the document body.

---

### Question 2: How does the `target="content"` attribute work with the `name` attribute of the iframe?
- **Model Answer**: When an `<a>` anchor tag has `target="content"`, the browser searches the current page for an embedded browsing context (an iframe or window) whose `name` attribute is `"content"`. When it finds it, it directs the URL into that frame instead of replacing the current tab.
- **Code Location**: `index.html` (navigation links in lines 22–26 matching iframe in line 35)
- **Likely Follow-Up**: *What is the default value of the `target` attribute if omitted?*
  - **Answer**: The default is `target="_self"`, which opens the link in the current frame or tab.

---

### Question 3: What are semantic HTML elements, and why did you use them?
- **Model Answer**: Semantic elements are tags whose names describe the meaning and purpose of their content to browsers, search engines, and screen readers. Instead of using generic `<div>` tags everywhere, I used `<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, and `<footer>`. This improves accessibility and makes the code cleaner.
- **Code Location**: `index.html` (header, nav, main, footer) and `articles.html` (sections and articles in lines 30–50)
- **Likely Follow-Up**: *What is the difference between `<section>` and `<article>`?*
  - **Answer**: An `<article>` is a self-contained piece of content that could stand alone (like a blog post or product card). A `<section>` is a thematic grouping of related content, often with a heading.

---

### Question 4: How did you implement the survey form in a tabular format?
- **Model Answer**: To satisfy the lab requirement, I wrapped an HTML `<table>` inside the `<form>`. Each row (`<tr>`) contains two cells: the left cell (`<td class="form-label-cell">`) holds the `<label>`, and the right cell (`<td class="form-input-cell">`) holds the interactive form control (`<input>`, `<select>`, `<textarea>`, or button group).
- **Code Location**: `survey.html` (lines 30–181)
- **Likely Follow-Up**: *How do you ensure accessibility when form labels are inside table cells?*
  - **Answer**: Every `<label>` has a `for` attribute matching the exact `id` of its corresponding input element (e.g. `<label for="studentEmail">` matches `<input id="studentEmail">`).

---

### Question 5: How do you make that tabular form responsive on mobile devices?
- **Model Answer**: On desktop screens, table cells naturally align side by side. In `style.css`, inside a media query for screens under 768px, I set `.form-table tr` to `display: flex; flex-direction: column;`. This forces the label cell and the input cell to stack vertically on top of each other on mobile phones.
- **Code Location**: `css/style.css` (lines 674–687)
- **Likely Follow-Up**: *What happens to the table borders on mobile?*
  - **Answer**: Each row retains a soft bottom border (`border-bottom: 1px solid var(--border-light)`), which visually separates the form fields like individual card sections.

---

### Question 6: What is the CSS Box Model, and why did you set `box-sizing: border-box`?
- **Model Answer**: The Box Model defines how elements occupy space: Content in the center, surrounded by Padding (internal cushion), Border (perimeter boundary), and Margin (external spacing between elements). By default in CSS, padding is added *on top* of an element's width. Setting `box-sizing: border-box` makes width include both padding and border, which prevents layout overflows.
- **Code Location**: `css/style.css` (lines 28–32)

---

### Question 7: What are CSS Custom Properties (Variables), and how did you use them?
- **Model Answer**: CSS Custom Properties allow us to store reusable values (like colors and font sizes) under custom names starting with `--`. I defined them in `:root` in `style.css` (such as `--background: #f5f5f7;` and `--text: #1d1d1f;`). Using variables makes it easy to maintain a consistent grayscale color scheme across all pages.
- **Code Location**: `css/style.css` (lines 6–25)
- **Likely Follow-Up**: *Why define them in `:root`?*
  - **Answer**: `:root` matches the top-level `<html>` element, ensuring the variables are inherited by every element on the page.

---

### Question 8: Where did you use Flexbox and where did you use CSS Grid?
- **Model Answer**: 
  - I used **Flexbox** for 1-dimensional layouts (a single row or column), such as the top navigation bar (`.header-inner`), horizontal navigation links (`.main-nav`), and the form action buttons.
  - I used **CSS Grid** for the 2-dimensional layout of model cards in `home.html` (`grid-template-columns: repeat(auto-fit, minmax(260px, 1fr))`), which automatically flows cards into multiple columns based on screen width.
- **Code Location**: `css/style.css` (Flexbox: line 93; Grid: line 236)

---

### Question 9: What does `event.preventDefault()` do in your survey form?
- **Model Answer**: In standard HTML, submitting a form triggers an HTTP request that causes the entire web page to reload. In single-page applications, we want JavaScript to validate the inputs and show the summary without losing the page state. Calling `e.preventDefault()` stops the browser's default reload behavior.
- **Code Location**: `js/script.js` (line 121)

---

### Question 10: How does the live search filter work in `models.html`?
- **Model Answer**: JavaScript attaches an `input` event listener to the search input. Every time the user types a character, the script converts the search query to lowercase and loops through all table rows (`<tr>`). It compares the query against each row's `textContent`. If there is a match, `row.style.display` is left as `""` (visible); if not, it is set to `"none"` (hidden).
- **Code Location**: `js/script.js` (lines 94–106)
- **Likely Follow-Up**: *Why use the `input` event instead of `change`?*
  - **Answer**: The `input` event fires immediately on every keystroke, enabling real-time live filtering. The `change` event only fires when the user leaves the input box or presses Enter.

---

### Question 11: What is the difference between `let` and `const` in JavaScript?
- **Model Answer**: Both declare block-scoped variables. `const` is used for variables that will not be reassigned (like references to DOM elements: `const form = document.getElementById(...)`). `let` is used for variables whose values will change over time (like our search match counter: `let matches = 0`).
- **Code Location**: `js/script.js` (lines 15, 96)

---

### Question 12: What is the difference between client-side validation and server-side validation?
- **Model Answer**: 
  - **Client-side validation** (which we implemented in `script.js`) runs in the user's browser, providing instant feedback (e.g. alert if email is missing `@`) before anything is sent over the network.
  - **Server-side validation** runs on a backend server (e.g. Node.js or Python). While client-side validation improves user experience, server-side validation is required for real security because client JavaScript can be disabled or bypassed.
- **Code Location**: `js/script.js` (lines 133–167)

---

### Question 13: Why did you put `novalidate` on the `<form>` tag in `survey.html`?
- **Model Answer**: The `novalidate` attribute disables the browser's default HTML5 validation bubble popups. This allowed our custom JavaScript to handle the validation checks, display friendly custom alerts, focus the invalid field, and build the dynamic summary card.
- **Code Location**: `survey.html` (line 28)

---

### Question 14: What is the security purpose of `rel="noopener noreferrer"` on external links?
- **Model Answer**: When an external link opens in a new tab (`target="_blank"`), the new page can access the original page using `window.opener` in JavaScript, which could lead to phishing attacks. `rel="noopener noreferrer"` closes this vulnerability and also prevents leaking referrer information.
- **Code Location**: `home.html` (lines 40, 54) and `models.html` (lines 55, 61)

---

### Question 15: What happens if a user opens `home.html` directly instead of `index.html`?
- **Model Answer**: Since `home.html` is designed to live inside the iframe, opening it directly could be confusing. In `home.html`, there is a hidden banner (`#standaloneNotice`). In `script.js`, line 71 checks `if (window.self !== window.top)`. If the page is NOT inside a frame, it reveals the banner with a button saying *"Open in Main View →"*, which links to `index.html` with `target="_top"`.
- **Code Location**: `home.html` (lines 13–16) and `js/script.js` (lines 82–86)

Now, review [GLOSSARY.md](GLOSSARY.md) for quick definitions of technical terms!
