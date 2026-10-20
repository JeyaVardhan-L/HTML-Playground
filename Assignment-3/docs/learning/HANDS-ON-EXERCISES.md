# Hands-On Exercises: Learn by Modifying

The best way to truly understand JavaScript is by modifying existing working code. 

Here are **8 small, guided exercises** ordered from easiest to most advanced. Try each exercise yourself, inspect the hint, and verify the expected result in your browser!

---

## Exercise 1 (Easy): Add a New Field (City) to the Registration Form

- **Goal**: Add a "City" text input to the form in Practical 1 and validate that it is not empty.
- **File to Edit**: `Assignment-3/practical-1-form.html`
- **Hint**:
  1. In the HTML (around line 140), add a new `.form-group` containing a label `<label for="city">City</label>`, `<input type="text" id="city">`, and `<span class="error-msg" id="cityError"></span>`.
  2. In the JavaScript (around line 265), read `const city = document.getElementById("city").value.trim();`.
  3. Add an `if (city === "") { setError("cityError", "City is required."); isValid = false; }`.
  4. In the success card template string, add `<li><strong>City:</strong> ${escapeHtml(city)}</li>`.
- **Expected Result**: Submitting with an empty city shows an error message in red. Entering a valid city includes it in the green success summary card.

---

## Exercise 2 (Easy): Change the Multiplier in the Practical 2 Loop

- **Goal**: Change the loop in Practical 2 from generating multiples of 3 to generating multiples of 7.
- **File to Edit**: `Assignment-3/practical-2-basics.html` (lines 375–379)
- **Hint**:
  Locate this loop in the `<script>` section:
  ```javascript
  for (let i = 1; i <= 5; i++) {
    loopResults.push(`Iteration ${i}: 3 * ${i} = ${3 * i}`);
  }
  ```
  Change `3` to `7`. Also change the paragraph description in line 164 to say *"First 5 multiples of 7"*.
- **Expected Result**: Reload `practical-2-basics.html`. Section 4 now displays `7 * 1 = 7`, `7 * 2 = 14`, `7 * 3 = 21`, etc.

---

## Exercise 3 (Easy–Medium): Add a 4th Overlapping Box to Practical 4

- **Goal**: Add "Box 4 (Amber Gold)" to the stacking stage in Practical 4.
- **File to Edit**: `Assignment-3/practical-4-stacking.html`
- **Hint**:
  1. In the CSS (around line 130), add styling for `#box4`:
     ```css
     #box4 {
       top: 195px;
       left: 340px;
       background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
       border: 2px solid #f59e0b;
       color: #92400e;
       z-index: 4;
     }
     ```
  2. In the HTML (around line 190), add `<div class="box" id="box4" data-name="Box 4 (Amber Gold)">...</div>`.
  3. In the JavaScript (line 219), change `let highestZIndex = 3;` to `let highestZIndex = 4;`.
- **Expected Result**: Four overlapping boxes now appear on screen. Clicking Box 4 brings it to the top with `z-index: 5`!

---

## Exercise 4 (Medium): Add a Character Counter to the Address Field

- **Goal**: In Practical 1, display a live count of characters remaining as the user types in the Address box.
- **File to Edit**: `Assignment-3/practical-1-form.html`
- **Hint**:
  1. Under the address textarea, add a small helper tag: `<small id="addressCounter">0 / 10 characters minimum</small>`.
  2. Add an `input` event listener in JavaScript:
     ```javascript
     const addressInput = document.getElementById("address");
     const addressCounter = document.getElementById("addressCounter");
     addressInput.addEventListener("input", function () {
       const len = addressInput.value.trim().length;
       addressCounter.textContent = `${len} / 10 characters minimum`;
       addressCounter.style.color = len >= 10 ? "#059669" : "#dc2626";
     });
     ```
- **Expected Result**: As you type into the address box, the counter updates in real time and turns green once you hit 10 characters.

---

## Exercise 5 (Medium): Add a Method to Calculate Rectangle Perimeter

- **Goal**: In Practical 2, add a new function that calculates the perimeter of a rectangle (`2 * (length + width)`).
- **File to Edit**: `Assignment-3/practical-2-basics.html`
- **Hint**:
  1. In Section 3, write the function:
     ```javascript
     function calculatePerimeter(length, width) {
       return 2 * (length + width);
     }
     ```
  2. Test invoking it in the console or by adding two input boxes and a button to the HTML.
- **Expected Result**: Calling `calculatePerimeter(10, 5)` returns `30`.

---

## Exercise 6 (Medium–Hard): Add a Double-Click Event to Practical 4

- **Goal**: Make double-clicking any box reset it to the bottom layer (`z-index: 1`).
- **File to Edit**: `Assignment-3/practical-4-stacking.html`
- **Hint**:
  In the `boxes.forEach(...)` loop, add a `dblclick` listener:
  ```javascript
  box.addEventListener("dblclick", function (event) {
    event.stopPropagation();
    this.style.zIndex = 1;
    const boxName = this.getAttribute("data-name");
    updateDisplay(`${boxName} sent to bottom`);
  });
  ```
- **Expected Result**: Single-clicking a box brings it to the top; double-clicking sends it behind the other cards.

---

## Exercise 7 (Hard): Add Drag Feedback to Target Zones in Practical 3

- **Goal**: When the star badge is dropped into Target Zone A or B, temporarily flash the zone's background color to gold.
- **File to Edit**: `Assignment-3/practical-3-drag-drop.html` (inside the `zone.addEventListener("drop", ...)` block)
- **Hint**:
  Inside the drop handler (around line 290):
  ```javascript
  zone.style.backgroundColor = "#fef08a"; // Flash yellow/gold
  setTimeout(function () {
    zone.style.backgroundColor = ""; // Reset after 500ms
  }, 500);
  ```
- **Expected Result**: Dropping the image into Zone A or B creates a satisfying yellow flash before returning to its normal background.

---

## Exercise 8 (Hard): Add Password Match Confirmation in Practical 1

- **Goal**: Add a "Confirm Password" input field and verify that both password fields match exactly.
- **File to Edit**: `Assignment-3/practical-1-form.html`
- **Hint**:
  1. Add an input `<input type="password" id="confirmPassword">` and `<span class="error-msg" id="confirmPasswordError"></span>`.
  2. In the `submit` listener:
     ```javascript
     const confirmPassword = document.getElementById("confirmPassword").value;
     if (confirmPassword === "") {
       setError("confirmPasswordError", "Please confirm your password.");
       isValid = false;
     } else if (confirmPassword !== password) {
       setError("confirmPasswordError", "Passwords do not match.");
       isValid = false;
     }
     ```
- **Expected Result**: If passwords differ, an error displays beside Confirm Password blocking form submission.

Now review the terminology cheat sheet in [GLOSSARY.md](GLOSSARY.md)!
