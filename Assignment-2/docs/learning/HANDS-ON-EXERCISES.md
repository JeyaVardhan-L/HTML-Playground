# Hands-On Exercises: Learn by Modifying

The best way to build confidence with code is by making small, deliberate edits and watching how the browser responds.

Here are 10 guided exercises ordered from easiest to most advanced. 

> [!TIP]
> **Try them first!** Complete solutions are intentionally not handed to you up front. Read the objective, check the hint, make your edit, and run the verification step.

---

## Exercise 1 (Easy): Change the Main Title & Subtitle

- **Objective**: Personalize the site brand in the top header.
- **Exact File to Edit**: `index.html` (lines 17–18)
- **Concept Taught**: Modifying text content inside HTML tags (`<span>`).
- **Hint**: Look inside `<div class="brand">` for `.brand-title` and `.brand-subtitle`. Replace `"Frontier AI Atlas"` with your custom title (e.g. `"Jey's AI Atlas"`).
- **Verification**: Refresh `index.html` in your browser. Verify the top left header shows your new title.

---

## Exercise 2 (Easy): Change the Page Background to a Warmer Gray

- **Objective**: Change the global background color of the entire website.
- **Exact File to Edit**: `css/style.css` (line 7)
- **Concept Taught**: CSS custom properties (variables) in `:root`.
- **Hint**: Locate `--background: #f5f5f7;` in `:root`. Try changing `#f5f5f7` to a warmer paper-like tone like `#f7f6f2` or a slightly cooler tone like `#eef0f3`.
- **Verification**: Refresh `index.html`. Notice that both the parent header background margins and the iframe background update simultaneously because all files share `style.css`.

---

## Exercise 3 (Easy–Medium): Add a 7th AI Model Card

- **Objective**: Add a card for **xAI Grok 3** to the model grid on the home page.
- **Exact File to Edit**: `home.html` (inside `<div class="cards-grid">`, around line 113)
- **Concept Taught**: HTML card structure using `<article>`, headings, and CSS Grid auto-flow.
- **Hint**: Copy one of the existing `<article class="model-card">` blocks. Change `.model-org` to `"xAI"`, `.model-title` to `"Grok 3"`, update the description, and set the link to `https://x.ai`.
- **Verification**: Refresh the home page. CSS Grid will automatically fit the 7th card into the grid layout without breaking neighboring cards.

---

## Exercise 4 (Medium): Add a "Release Year" Column to the Table

- **Objective**: Add a 5th column named "Release Year" to the comparison matrix.
- **Exact File to Edit**: `models.html` (lines 43–87)
- **Concept Taught**: HTML table structure (`<th>`, `<td>`, and aligning row cells).
- **Hint**: 
  1. Add `<th scope="col">Release Year</th>` to the `<thead>` row.
  2. In the `<tbody>`, add a matching `<td>2024</td>` or `<td>2025</td>` to every single `<tr>`.
- **Verification**: Reload `models.html`. Verify the table now displays 5 neatly aligned columns.

---

## Exercise 5 (Medium): Add an "Expert / Researcher" Survey Option

- **Objective**: Add a 4th choice to the Experience Level radio button group.
- **Exact File to Edit**: `survey.html` (lines 110–123)
- **Concept Taught**: Form input grouping, radio button `name` attributes, and accessibility.
- **Hint**: Inside `<div class="options-group">`, add another `<label class="option-item">` containing an `<input type="radio" name="experience" value="Expert">` with the text `"Expert / Researcher"`.
- **Verification**: Open `survey.html`, select your new option, and click "Submit Survey". Confirm that "Expert" appears under **Experience Level** in the result summary list!

---

## Exercise 6 (Medium): Change the Corner Radius of Cards

- **Objective**: Give all cards a sleeker, boxier industrial look or a softer pill look.
- **Exact File to Edit**: `css/style.css` (line 15)
- **Concept Taught**: Global border-radius design tokens.
- **Hint**: Locate `--radius: 12px;` in `:root`. Try setting it to `4px` for a crisp geometric look, or `24px` for a bubbly modern look.
- **Verification**: Inspect `home.html` and `survey.html`. All model cards, table wrappers, and form containers will update their corners together.

---

## Exercise 7 (Medium–Hard): Adjust the Mobile Responsive Breakpoint

- **Objective**: Change when the mobile layout kicks in.
- **Exact File to Edit**: `css/style.css` (line 659)
- **Concept Taught**: CSS Media Queries (`@media (max-width: ...)`).
- **Hint**: Locate `@media (max-width: 768px)`. Change `768px` to `600px` (standard phone width) or `900px` (small tablet width).
- **Verification**: In your browser, open Developer Tools (F12 or right-click -> Inspect). Drag the window width back and forth to observe the exact pixel point where the header and form switch to vertical stacking.

---

## Exercise 8 (Hard): Highlight the Number of Search Results

- **Objective**: When the search filter in `models.html` finds zero matches, change the counter text to red.
- **Exact File to Edit**: `js/script.js` (lines 108–111)
- **Concept Taught**: DOM manipulation, conditional logic, and inline CSS styles via JavaScript.
- **Hint**: Inside the `input` event listener, check if `matches === 0`. If so, set `countDisplay.style.color = "#d93025";` and text to `"No models match your search"`. Otherwise, reset `countDisplay.style.color = "";`.
- **Verification**: Go to the Models tab and type `"xyz123"`. Confirm the text turns red and informs you that nothing matched.

---

## Exercise 9 (Hard): Add a Minimum Name Length Validation Rule

- **Objective**: In the survey form, reject any name shorter than 3 characters with a helpful alert.
- **Exact File to Edit**: `js/script.js` (lines 134–138)
- **Concept Taught**: JavaScript string properties (`.length`), conditional checks, and form validation flows.
- **Hint**: Add an `else if (name.length < 3)` condition right below `if (!name)`. Show an alert like `"Name must be at least 3 characters long."` and call `document.getElementById("studentName").focus();`.
- **Verification**: Go to the Survey page. Type `"Al"` as your name, fill the other fields, and click Submit. Confirm the validation alert blocks submission!

---

## Exercise 10 (Advanced): Trace the Iframe Auto-Resize Handshake

- **Objective**: Understand and log the communication between subpages and parent window.
- **Exact Files to Inspect**: `js/script.js` (lines 58–62 and lines 71–79)
- **Concept Taught**: Cross-window communication (`window.parent.postMessage` and `window.addEventListener("message")`).
- **Hint**:
  1. Add a `console.log("Sending height from subpage:", height);` inside `sendHeight()` (line 76).
  2. Add a `console.log("Parent received resize message:", event.data);` inside the parent message listener (line 59).
- **Verification**: Open browser DevTools Console (F12). Click between "Home", "Articles", and "Models". Watch the messages log in the console as subpages calculate their height and send it up to the parent shell.

Ready to test your theoretical knowledge? Proceed to [VIVA-PREP.md](VIVA-PREP.md)!
