# JavaScript From Zero: How Interactivity Works

This guide explains how **JavaScript** adds behavior, search filtering, form validation, and frame management to **Frontier AI Atlas**. Every concept, variable, and function discussed here comes directly from `js/script.js`.

---

## 1. What Does JavaScript Do Here?

JavaScript is a programming language that runs inside the web browser. 

In this assignment, **there is no database or server-side backend**. JavaScript runs purely on the user's computer (client-side) to:
1. Highlight active navigation links when clicked.
2. Filter table rows instantly as you type in the search bar.
3. Validate user entries in the survey form before submission.
4. Construct and display a dynamic summary of survey responses.
5. Automatically resize the iframe so content doesn't get clipped.

---

## 2. Core Concepts Present in Our Code

### A. Variables (`const` and `let`)
Variables store data or references to HTML elements in memory:
- `const`: Used when the variable will never be reassigned.
  ```javascript
  const iframe = document.getElementById("content-frame");
  const navLinks = document.querySelectorAll(".nav-link");
  ```
- `let`: Used when the value changes over time (such as a counter).
  ```javascript
  let matches = 0; // increments as matching table rows are found
  ```

### B. Functions
A function is a reusable block of code that performs an action when called:
```javascript
// Named function definition
function escapeText(str) {
  if (!str) return "";
  return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}
```

### C. The DOM (Document Object Model)
When the browser loads an HTML document, it creates an in-memory tree of objects representing every tag on the page. JavaScript interacts with this tree using DOM queries:
- `document.getElementById("studentName")`: Finds the single element with that ID.
- `document.querySelector('input[name="experience"]:checked')`: Finds the first element matching a CSS selector (e.g. the checked radio button).
- `document.querySelectorAll("#modelTableBody tr")`: Finds a list (NodeList) of all matching elements.

### D. Events and Event Listeners
An **event** is something that happens in the browser—like a user clicking a button (`click`), typing in an input (`input`), submitting a form (`submit`), or resizing the browser window (`resize`).

An **event listener** is a function that waits for an event and runs code in response:
```text
  [HTML Element]  --- listens for --->  [Event: "click"]  --->  [Callback Function runs]
```

Example in `script.js` (lines 6–9):
```javascript
document.addEventListener("DOMContentLoaded", function () {
  initParentNavigation();
  initSubpageFeatures();
});
```
`DOMContentLoaded` fires as soon as the HTML has finished loading into memory, guaranteeing our script does not attempt to find elements before they exist.

---

## 3. What the Browser Does vs. What Our JavaScript Does

Before inspecting the features, it helps to distinguish the browser's automatic actions from our custom JavaScript logic:

| Action | Done Automatically by the Browser | Handled by Our JavaScript (`script.js`) |
| :--- | :--- | :--- |
| **Navigating inside the Iframe** | Yes. Browser reads `target="content"` and loads the page into `<iframe name="content">`. | Adds the `.active` styling pill to the clicked link and syncs the URL name. |
| **Resetting the Survey Form** | Yes. `<button type="reset">` automatically clears all input text, unchecks boxes, and restores defaults. | Hides the submission summary card (`#surveyResultCard`). |
| **Filtering the Models Table** | No. The browser has no native ability to filter HTML tables based on search input. | Yes. Captures the `input` event and toggles `row.style.display`. |
| **Validating the Survey Form** | Partially. HTML5 attributes like `required` provide default browser tooltips. | Yes. We added `novalidate` to the form to take full control, displaying custom alerts and generating the response summary. |

---

## 4. Feature 1: Model Table Live Search (`models.html`)

Located in `js/script.js` (lines 89–112).

### The Trigger:
The user types any letter into `<input type="search" id="modelSearch">`.

### Sequence of Execution:
```text
1. User types "math" into search input
       |
       v
2. "input" event fires immediately on each keystroke
       |
       v
3. JS extracts query: query = e.target.value.toLowerCase().trim()  --> "math"
       |
       v
4. Loops through each table row: tableRows.forEach(row => { ... })
       |
       v
5. Extracts all text inside row: text = row.textContent.toLowerCase()
       |
       +---> If text contains "math": row.style.display = ""    (visible)
       |                              matches++
       |
       +---> If text does NOT contain "math": row.style.display = "none" (hidden)
       |
       v
6. Updates counter text: "Showing 2 of 6 models"
```

### The Actual Code:
```javascript
searchInput.addEventListener("input", function (e) {
  const query = e.target.value.toLowerCase().trim();
  let matches = 0;

  tableRows.forEach((row) => {
    const text = row.textContent.toLowerCase();
    if (!query || text.includes(query)) {
      row.style.display = ""; // Default display (table-row)
      matches++;
    } else {
      row.style.display = "none"; // Hides row from render tree
    }
  });

  if (countDisplay) {
    countDisplay.textContent = `Showing ${matches} of ${tableRows.length} models`;
  }
});
```

---

## 5. Feature 2: Survey Form Validation & Summary (`survey.html`)

Located in `js/script.js` (lines 115–192).

### The Trigger:
The user clicks the `<button type="submit">Submit Survey</button>`.

### Step 1: Stopping the Default Reload
```javascript
surveyForm.addEventListener("submit", function (e) {
  e.preventDefault();
```
Normally, submitting an HTML form sends an HTTP request and reloads the entire page. Calling `e.preventDefault()` halts this default behavior so our JavaScript can handle the data client-side.

### Step 2: Extracting Values
```javascript
const name = document.getElementById("studentName").value.trim();
const email = document.getElementById("studentEmail").value.trim();
const model = document.getElementById("favModel").value;
const useCase = document.getElementById("primaryUseCase").value;
const expRadio = surveyForm.querySelector('input[name="experience"]:checked');
const comments = document.getElementById("surveyComments").value.trim() || "None";

// Gather all checked capability checkboxes into an array of strings
const selectedCheckboxes = surveyForm.querySelectorAll('input[name="capabilities"]:checked');
const capabilities = Array.from(selectedCheckboxes).map((cb) => cb.value);
```

### Step 3: Sequential Validation Checks
If any required field is missing or invalid, an alert is shown, the cursor is focused into the offending field, and the function terminates early (`return;`):
```javascript
if (!name) {
  alert("Please enter your name.");
  document.getElementById("studentName").focus();
  return;
}
if (!email || !email.includes("@")) {
  alert("Please enter a valid email address.");
  document.getElementById("studentEmail").focus();
  return;
}
if (!model) { ... }
if (!useCase) { ... }
if (!expRadio) { ... }
if (capabilities.length === 0) { ... }
```

### Step 4: Building the Summary Card
If all checks pass, JavaScript generates formatted HTML and injects it into `<ul id="summaryList">`:
```javascript
summaryList.innerHTML = `
  <li><strong>Student Name:</strong> ${escapeText(name)}</li>
  <li><strong>Email:</strong> ${escapeText(email)}</li>
  <li><strong>Favorite Model:</strong> ${escapeText(model)}</li>
  <li><strong>Primary Use Case:</strong> ${escapeText(useCase)}</li>
  <li><strong>Experience Level:</strong> ${escapeText(expRadio.value)}</li>
  <li><strong>Capabilities:</strong> ${capabilities.map(c => escapeText(c)).join(", ")}</li>
  <li><strong>Comments:</strong> ${escapeText(comments)}</li>
`;

// Make the hidden card visible
resultCard.style.display = "block";
```

### Step 5: Sanitizing Text with `escapeText`
To protect against HTML injection (XSS), any user-submitted string is escaped before being inserted into `innerHTML`:
```javascript
function escapeText(str) {
  if (!str) return "";
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}
```

---

## 6. Feature 3: Resetting the Form

In `survey.html`, line 175 is:
```html
<button type="reset" class="btn btn-secondary">Reset</button>
```
When clicked:
1. The **browser natively resets** all text inputs to empty strings, resets selects to their first option, and restores initial checkbox checks.
2. Our **JavaScript listener** (lines 194–198) simply hides the summary card:
   ```javascript
   surveyForm.addEventListener("reset", function () {
     if (resultCard) {
       resultCard.style.display = "none";
     }
   });
   ```

---

## 7. Feature 4: Iframe Navigation & Auto-Resizing

In `script.js` (lines 14–64 and 71–86), there is code that keeps the iframe smooth and synchronized.

### A. Navigation Tab Highlighting (lines 19–25)
When a navigation link is clicked:
```javascript
navLinks.forEach((link) => {
  link.addEventListener("click", function () {
    navLinks.forEach((l) => l.classList.remove("active"));
    this.classList.add("active");
    window.scrollTo({ top: 0, behavior: "smooth" });
  });
});
```

### B. An Honest Note on Complexity: `postMessage` Auto-Resizing
Lines 28–63 and 71–81 implement automatic iframe height adjustment using `postMessage` and `scrollHeight`:

> [!NOTE]
> **Honest Assessment for Beginners**:
> In standard introductory lab assignments, an `<iframe>` is usually given a fixed CSS height (such as `height: 800px;` or `height: 100vh;`). 
> 
> However, because our subpages have different lengths (e.g. `articles.html` is longer than `models.html`), a fixed height causes double scrollbars. To solve this, our code uses `window.parent.postMessage({ type: "ATLAS_RESIZE", height: ... }, "*")` to measure the subpage's scroll height and adjust the iframe's height dynamically.
> 
> You do **not** need to memorize `postMessage` for basic HTML/CSS exams. If an examiner asks, simply explain: *"We added an event listener that measures the document height and resizes the iframe so the user never sees nested vertical scrollbars."*

Now that you understand the JavaScript logic, explore [CODE-TOUR.md](CODE-TOUR.md) for a file-by-file walkthrough!
