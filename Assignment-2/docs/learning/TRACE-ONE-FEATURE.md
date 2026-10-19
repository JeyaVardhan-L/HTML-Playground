# Tracing Three Real Features Step-by-Step

To truly understand how this website functions, let's trace the execution path of three real user workflows from the moment the user clicks or types to the final visual update.

---

## Workflow A: Clicking "Models" in Navigation

### The Scenario:
The user is viewing the home page inside `index.html` and clicks the **"Models"** tab in the top navigation bar.

### Trace of Execution:

```text
[User Clicks "Models" Link in index.html]
                  |
                  v
[Step 1: HTML Link Inspection]
   <a href="models.html" target="content" class="nav-link" id="nav-models">Models</a>
                  |
                  v
[Step 2: Browser Frame Targeting]
   Browser matches target="content" to <iframe name="content" ...>
   Loads models.html INSIDE the iframe viewport without reloading index.html
                  |
                  v
[Step 3: JavaScript Click Listener Fires]
   navLinks.forEach(l => l.classList.remove("active"))
   this.classList.add("active")
   window.scrollTo({ top: 0, behavior: "smooth" })
                  |
                  v
[Step 4: Iframe Auto-Resize Synchronization]
   iframe triggers "load" event -> resizeIframe() measures scrollHeight
   Adjusts iframe height to prevent double scrollbars
```

### 1. Which link is clicked?
In `index.html` (line 23):
```html
<a href="models.html" target="content" class="nav-link" id="nav-models">Models</a>
```

### 2. How does the iframe receive the page?
In `index.html` (lines 33–39), the iframe is declared with `name="content"`:
```html
<iframe src="home.html" name="content" id="content-frame" ...></iframe>
```
Because the clicked anchor tag has `target="content"`, standard HTML specification instructs the browser to open the URL (`models.html`) inside the browsing context named `"content"`.

### 3. Why does the parent page remain visible?
Standard hyperlinks without a `target` navigate the entire browser window (technically `target="_self"`). By directing the request into the named `<iframe>`, only the DOM inside the iframe is destroyed and rebuilt. The parent document (`index.html`)—including the header, brand title, active nav bar, and footer—remains permanently in memory.

### 4. How does the active navigation state change?
In `js/script.js` (lines 19–25):
```javascript
navLinks.forEach((link) => {
  link.addEventListener("click", function () {
    // 1. Remove .active from all navigation links
    navLinks.forEach((l) => l.classList.remove("active"));
    // 2. Add .active to the currently clicked link
    this.classList.add("active");
    // 3. Smoothly scroll parent viewport to top
    window.scrollTo({ top: 0, behavior: "smooth" });
  });
});
```
In `css/style.css` (lines 143–147), `.nav-link.active` applies the highlighted pill appearance:
```css
.nav-link.active {
  background-color: #e5e5ea;
  color: #000000;
  font-weight: 600;
}
```

---

## Workflow B: Searching for a Model

### The Scenario:
The user is viewing `models.html` and types `"deepseek"` into the search bar.

### Trace of Execution:

```text
[User types "deepseek" in #modelSearch]
                  |
                  v
[Step 1: "input" Event Fires]
   searchInput.addEventListener("input", function (e) { ... })
                  |
                  v
[Step 2: Input Extraction & Normalization]
   query = e.target.value.toLowerCase().trim()  --> "deepseek"
                  |
                  v
[Step 3: Table Row Iteration]
   tableRows.forEach((row) => {
     text = row.textContent.toLowerCase()
                  |
                  +---> Row contains "deepseek"?
                  |        YES: row.style.display = ""     (Keep visible)
                  |             matches++
                  |        NO:  row.style.display = "none" (Hide row)
   })
                  |
                  v
[Step 4: Counter Display Updated]
   countDisplay.textContent = `Showing 1 of 6 models`
```

### 1. What event occurs?
The browser fires the `input` event on `<input type="search" id="modelSearch">`. Unlike the `change` event (which waits until the user presses Enter or clicks away), `input` fires immediately after **every single keystroke**.

### 2. How is the input read?
In `js/script.js` (lines 94–96):
```javascript
searchInput.addEventListener("input", function (e) {
  const query = e.target.value.toLowerCase().trim();
  let matches = 0;
```
- `e.target.value`: Extracts the raw text currently in the box.
- `.toLowerCase()`: Normalizes the search so typing `"DeepSeek"`, `"deepseek"`, or `"DEEPSEEK"` all match.
- `.trim()`: Strips accidental leading or trailing spaces.

### 3. How are table rows checked?
In `js/script.js` (lines 98–106):
```javascript
tableRows.forEach((row) => {
  const text = row.textContent.toLowerCase();
  if (!query || text.includes(query)) {
    row.style.display = "";
    matches++;
  } else {
    row.style.display = "none";
  }
});
```
- `row.textContent`: Gathers **all** text from every cell (`<td>`) in that row—including the organization, model name, and capabilities.
- `text.includes(query)`: Checks if the row's text contains the search query.

### 4. How does the browser display matching results?
- If it matches: `row.style.display = ""` clears any inline hiding, allowing CSS to display the row normally as a table row.
- If it does not match: `row.style.display = "none"` removes the row from the visual layout entirely.
- Finally, the matching count updates:
  ```javascript
  countDisplay.textContent = `Showing ${matches} of ${tableRows.length} models`;
  ```

---

## Workflow C: Submitting the Developer Survey

### The Scenario:
The user fills out `survey.html` and clicks the **"Submit Survey"** button.

### Trace of Execution:

```text
[User clicks "Submit Survey" button]
                  |
                  v
[Step 1: Intercept Default Submission]
   surveyForm.addEventListener("submit", function (e) {
     e.preventDefault(); // Prevents page reload / HTTP POST
                  |
                  v
[Step 2: Extract & Inspect Field Values]
   Extracts: name, email, model, useCase, expRadio, capabilities, comments
                  |
                  v
[Step 3: Sequential Validation]
   !name?               -> alert("Please enter your name.") & focus()
   !email.includes('@')?-> alert("Please enter a valid email address.") & focus()
   !model?              -> alert("Please select your favorite AI model.")
   !expRadio?           -> alert("Please select your experience level.")
   !capabilities.length?-> alert("Please select at least one capability...")
                  |
                  v (All checks pass!)
[Step 4: Generate Results Summary]
   summaryList.innerHTML = `<li><strong>Student Name:</strong> ${escapeText(name)}</li>...`
   resultCard.style.display = "block"
                  |
                  v
[Step 5: Reset Behavior (If Reset Clicked)]
   Browser clears inputs natively
   surveyForm.addEventListener("reset", ...) hides #surveyResultCard
```

### 1. How does HTML validation work?
In `survey.html` (line 28), the form tag includes `novalidate`:
```html
<form id="aiSurveyForm" novalidate>
```
Although individual inputs retain `required` and `type="email"`, the `novalidate` attribute tells the browser: *"Do not show standard native popups; let our custom JavaScript handle validation logic."*

### 2. Which JavaScript event runs?
The form's `submit` event fires when the user clicks the `<button type="submit">` or presses Enter inside an input field.

### 3. Why is default form submission prevented?
In `js/script.js` (line 121):
```javascript
e.preventDefault();
```
Without `preventDefault()`, the browser would treat the form as an old-fashioned HTTP submission, refreshing the page and erasing all entries! Calling `preventDefault()` keeps the page in place so JavaScript can validate the data client-side.

### 4. How is the summary produced?
In `js/script.js` (lines 170–183):
```javascript
if (summaryList) {
  summaryList.innerHTML = `
    <li><strong>Student Name:</strong> ${escapeText(name)}</li>
    <li><strong>Email:</strong> ${escapeText(email)}</li>
    <li><strong>Favorite Model:</strong> ${escapeText(model)}</li>
    <li><strong>Primary Use Case:</strong> ${escapeText(useCase)}</li>
    <li><strong>Experience Level:</strong> ${escapeText(expRadio.value)}</li>
    <li><strong>Capabilities:</strong> ${capabilities.map(c => escapeText(c)).join(", ")}</li>
    <li><strong>Comments:</strong> ${escapeText(comments)}</li>
  `;
}

if (resultCard) {
  resultCard.style.display = "block";
}
```
The summary card (`#surveyResultCard`), which was previously hidden via `display: none;` in `css/style.css`, is set to `display: block;` to reveal the user's responses.

### 5. What happens on reset?
In `survey.html` (line 175):
```html
<button type="reset" class="btn btn-secondary">Reset</button>
```
When clicked:
1. The **browser automatically clears** all text boxes, resets dropdowns, and unchecks boxes.
2. In `js/script.js` (lines 194–198), our reset listener cleanly hides the summary card:
   ```javascript
   surveyForm.addEventListener("reset", function () {
     if (resultCard) {
       resultCard.style.display = "none";
     }
   });
   ```

Now that you can trace these features, test your skills with [HANDS-ON-EXERCISES.md](HANDS-ON-EXERCISES.md)!
