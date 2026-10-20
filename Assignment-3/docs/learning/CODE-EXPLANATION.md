# Code Explanation: Program-by-Program Walkthrough

This guide walks through the complete source code of all four practicals in **Assignment 3**. For each program, you will find its purpose, HTML elements, CSS highlights, JavaScript logic, execution flow, interaction traces, and exact code snippets.

---

## Program 1: `practical-1-form.html` (Registration Form with Validation)

### 1. Purpose & Syllabus Topics Covered
- **Purpose**: Validates student inputs on the client side before allowing registration, displaying field-level errors or a success card.
- **Topics Demonstrated**: Functions, Variables (`let`, `const`), Data Types, Expressions, Control Statements (`if/else if/else`), DOM Methods, Form Events (`submit`, `reset`), and `event.preventDefault()`.

### 2. Key HTML Elements
- `<form id="registrationForm" novalidate>`: The container for all input controls. `novalidate` prevents default browser validation balloons so custom JavaScript executes.
- `<input type="text" id="fullName">`, `<input type="number" id="age">`, `<input type="email" id="email">`, `<input type="text" id="phone">`, `<textarea id="address">`, `<input type="password" id="password">`.
- `<input type="radio" name="gender" value="...">`: Radio buttons sharing `name="gender"` for mutual exclusion.
- `<span class="error-msg" id="nameError"></span>`: Dedicated empty error spans placed under each field to hold dynamic error messages.
- `<div id="successCard" class="success-card">`: Hidden result card (`display: none`) revealed only when all checks pass.

### 3. Key JavaScript Code Snippets

#### A. DOM Selection & Helper Functions
```javascript
// Selecting the form and output targets
const form = document.getElementById("registrationForm");
const successCard = document.getElementById("successCard");
const summaryList = document.getElementById("summaryList");

// Helper function to show an error message beside a specific field
function setError(elementId, message) {
  const errorSpan = document.getElementById(elementId);
  if (errorSpan) {
    errorSpan.textContent = message;
  }
}

// Helper function to clear all error messages
function clearAllErrors() {
  const errorSpans = document.querySelectorAll(".error-msg");
  errorSpans.forEach(function (span) {
    span.textContent = "";
  });
}
```
- **Why it matters**: `setError()` abstracts the DOM lookup and text assignment, keeping the validation code tidy and readable.

#### B. Intercepting Form Submission & Halting Reload
```javascript
form.addEventListener("submit", function (event) {
  event.preventDefault(); // STOPS the browser from reloading the page
  clearAllErrors();
  successCard.style.display = "none";
  let isValid = true;
```
- **Why `event.preventDefault()` is vital**: Without this line, the browser sends an HTTP request and reloads the page, wiping out all inputs and error messages instantly.

#### C. Reading Values & Validation Logic
```javascript
const fullName = document.getElementById("fullName").value.trim();
const ageValue = document.getElementById("age").value.trim();
const ageNumber = Number(ageValue);

// Name Validation
if (fullName === "") {
  setError("nameError", "Full Name is required.");
  isValid = false;
} else if (fullName.length < 3) {
  setError("nameError", "Name must be at least 3 characters long.");
  isValid = false;
}

// Age Validation
if (ageValue === "") {
  setError("ageError", "Age is required.");
  isValid = false;
} else if (isNaN(ageNumber) || ageNumber < 18 || ageNumber > 100) {
  setError("ageError", "Please enter a valid age between 18 and 100.");
  isValid = false;
}
```

#### D. Success Card Display
```javascript
if (isValid) {
  summaryList.innerHTML = `
    <li><strong>Name:</strong> ${escapeHtml(fullName)}</li>
    <li><strong>Age:</strong> ${ageNumber}</li>
    <li><strong>Email:</strong> ${escapeHtml(email)}</li>
    <li><strong>Phone:</strong> ${escapeHtml(phone)}</li>
    <li><strong>Gender:</strong> ${genderRadio.value}</li>
    <li><strong>Address:</strong> ${escapeHtml(address)}</li>
  `;
  successCard.style.display = "block"; // DHTML: reveals the green success box
}
```

### 4. Step-by-Step Interaction Trace
1. **User clicks "Register" with empty fields**:
   - `submit` event fires → `event.preventDefault()` stops page reload.
   - `fullName === ""` evaluates to `true` → `setError("nameError", ...)` writes text into `#nameError`.
   - `isValid` becomes `false`.
   - Process repeats for age, email, phone, address, password, and gender.
   - `if (isValid)` fails; `successCard` remains hidden.
2. **User enters valid values and clicks "Register"**:
   - All validation conditions pass (`isValid` stays `true`).
   - `summaryList.innerHTML` is populated with the student's data.
   - `successCard.style.display = "block"` makes the green box visible.
3. **User clicks "Reset"**:
   - Browser clears inputs natively; our `reset` listener clears all error spans and hides `successCard`.

---

## Program 2: `practical-2-basics.html` (Core JS Foundations & Objects)

### 1. Purpose & Syllabus Topics Covered
- **Purpose**: An interactive laboratory demonstrating fundamental language concepts in self-contained visual panels.
- **Topics Demonstrated**: Data Types (`typeof`), Expressions, Functions with Return Values, `if/else`, `for` loop, JavaScript Objects with Methods (`this`), the `Date` Object, String Methods, and Error Handling (`try/catch/finally`).

### 2. Key Code Snippets by Section

#### Section 1: Primitive Data Types Table
```javascript
const sampleString = "Frontier AI";
const sampleNumber = 42;
const sampleBoolean = true;
const sampleUndefined = undefined;
const sampleNull = null;

const typesData = [
  { type: "String", val: `"${sampleString}"`, evaluated: typeof sampleString },
  { type: "Number", val: `${sampleNumber}`, evaluated: typeof sampleNumber },
  { type: "Boolean", val: `${sampleBoolean}`, evaluated: typeof sampleBoolean },
  { type: "Undefined", val: "undefined", evaluated: typeof sampleUndefined },
  { type: "Null", val: "null", evaluated: `${typeof sampleNull} (historic JS behavior)` }
];
```
- Demonstrates how the `typeof` operator inspects variable types dynamically at runtime.

#### Section 3: Function with Parameters & Return Value
```javascript
function calculateCircleArea(radius) {
  const area = Math.PI * radius * radius;
  return area.toFixed(2); // sends formatted string back to caller
}

calcAreaBtn.addEventListener("click", function () {
  const radius = parseFloat(document.getElementById("circleRadius").value);
  const result = calculateCircleArea(radius);
  funcOutput.innerHTML = `Function Call: <code>calculateCircleArea(${radius})</code> returned: <strong>${result} sq. units</strong>`;
});
```

#### Section 4: Loops and Conditionals
```javascript
// for loop generating multiples of 3
const loopResults = [];
for (let i = 1; i <= 5; i++) {
  loopResults.push(`Iteration ${i}: 3 * ${i} = ${3 * i}`);
}
document.getElementById("loopOutput").textContent = loopResults.join("\n");
```

#### Section 5: JavaScript Object with Properties & Method
```javascript
const student = {
  name: "Jey",
  rollNo: "9057",
  course: "Computer Science",
  marks: [85, 90, 88],
  // Method using 'this' keyword to access its own properties
  calculateAverage: function () {
    let total = 0;
    for (let i = 0; i < this.marks.length; i++) {
      total += this.marks[i];
    }
    return (total / this.marks.length).toFixed(1);
  }
};

// Calling the object method:
student.calculateAverage(); // returns "87.7"
```

#### Section 8: Error Handling (`try / throw / catch / finally`)
```javascript
function divideNumbers(x, y) {
  if (y === 0) {
    throw new Error("ZeroDivisionError: Cannot divide a number by zero!");
  }
  return x / y;
}

divideBtn.addEventListener("click", function () {
  const valA = parseFloat(document.getElementById("numA").value);
  const valB = parseFloat(document.getElementById("numB").value);

  try {
    const quotient = divideNumbers(valA, valB);
    errorOutput.innerHTML = `✓ Success: ${valA} ÷ ${valB} = ${quotient}`;
  } catch (err) {
    // Gracefully catches the thrown error without crashing the script
    errorOutput.className = "output-box error-out";
    errorOutput.innerHTML = `⚠ Caught Error: <strong>${err.message}</strong>`;
  } finally {
    // Runs in both success and error cases
    errorOutput.innerHTML += `<br><small>(finally block executed)</small>`;
  }
});
```

---

## Program 3: `practical-3-drag-drop.html` (Drag and Drop Image)

### 1. Purpose & Syllabus Topics Covered
- **Purpose**: Implements the HTML5 Drag-and-Drop specification with a local SVG image, allowing the user to reposition the image inside a canvas or drop it into target zones.
- **Topics Demonstrated**: Events (`dragstart`, `dragend`, `dragover`, `dragenter`, `dragleave`, `drop`), `dataTransfer`, Coordinates, DOM manipulation, and DHTML.

### 2. Key Elements & Drag-and-Drop Architecture
- `<div class="drag-canvas" id="canvasArea">`: The bordered drop area with `position: relative`.
- `<img src="assets/star.svg" id="dragImage" draggable="true">`: Draggable badge using `draggable="true"`.
- `<div class="drop-zone" id="zoneA">`: Designated sub-target drop bins.
- `<div class="log-container" id="eventLog">`: Real-time timestamped event log displaying each fired event.

### 3. Key JavaScript Code Snippets

#### Step 1: Starting the Drag (`dragstart`)
```javascript
dragImage.addEventListener("dragstart", function (event) {
  // 1. Calculate offset where the mouse grabbed the image
  const rect = dragImage.getBoundingClientRect();
  grabOffsetX = event.clientX - rect.left;
  grabOffsetY = event.clientY - rect.top;

  // 2. Set dataTransfer payload
  event.dataTransfer.setData("text/plain", dragImage.id);
  event.dataTransfer.effectAllowed = "move";

  // 3. DHTML styling: reduce opacity while dragging
  dragImage.classList.add("dragging");
  logEvent("dragstart", "User began dragging image.");
});
```

#### Step 2: Enabling the Canvas to Accept Drops (`dragover`)
```javascript
canvasArea.addEventListener("dragover", function (event) {
  event.preventDefault(); // MANDATORY! By default, browsers forbid drops on elements
  event.dataTransfer.dropEffect = "move";
});
```
> [!IMPORTANT]
> In HTML5 Drag and Drop, calling `event.preventDefault()` inside `dragover` is **required**. If you omit this, the browser will never fire the `drop` event!

#### Step 3: Dropping on Canvas & Updating Position (DHTML)
```javascript
canvasArea.addEventListener("drop", function (event) {
  event.preventDefault();
  canvasArea.classList.remove("drag-over");

  // Calculate mouse drop position relative to canvas
  const canvasRect = canvasArea.getBoundingClientRect();
  let newLeft = event.clientX - canvasRect.left - grabOffsetX;
  let newTop = event.clientY - canvasRect.top - grabOffsetY;

  // Keep image within canvas boundaries
  const maxLeft = canvasArea.clientWidth - dragImage.offsetWidth;
  const maxTop = canvasArea.clientHeight - dragImage.offsetHeight;
  newLeft = Math.max(0, Math.min(newLeft, maxLeft));
  newTop = Math.max(0, Math.min(newTop, maxTop));

  // DHTML: Dynamically update inline CSS positioning
  dragImage.style.left = newLeft + "px";
  dragImage.style.top = newTop + "px";

  logEvent("drop", `Image placed at (${Math.round(newLeft)}, ${Math.round(newTop)})`);
});
```

---

## Program 4: `practical-4-stacking.html` (Dynamic Stacking using z-index)

### 1. Purpose & Syllabus Topics Covered
- **Purpose**: Displays three overlapping colored boxes. Clicking any box dynamically brings it to the top of the stack.
- **Topics Demonstrated**: CSS `z-index`, CSS positioning (`absolute` inside `relative`), DOM selection (`querySelectorAll`), Event Listeners (`click`), and DHTML.

### 2. Key Code Snippets

#### A. Initial CSS Positioning & Overlap
```css
.stack-stage {
  position: relative; /* Container boundary */
  height: 360px;
}

.box {
  position: absolute; /* Allows manual positioning and z-index */
  width: 220px;
  height: 170px;
}

#box1 { top: 30px;  left: 40px;  z-index: 1; }
#box2 { top: 85px;  left: 140px; z-index: 2; }
#box3 { top: 140px; left: 240px; z-index: 3; }
```

#### B. The Dynamic Stacking Logic
```javascript
// Initialize counter to match the highest initial layer
let highestZIndex = 3;

const boxes = document.querySelectorAll(".box");

boxes.forEach(function (box) {
  box.addEventListener("click", function () {
    // 1. Increment the depth counter
    highestZIndex++;

    // 2. DHTML: Apply new z-index to the clicked element
    this.style.zIndex = highestZIndex;

    // 3. Update the live status display
    const boxName = this.getAttribute("data-name");
    updateDisplay(boxName);
  });
});
```

### 3. Step-by-Step Interaction Trace
1. **Initial State**:
   - Box 1 has `z-index: 1` (bottom).
   - Box 2 has `z-index: 2` (middle).
   - Box 3 has `z-index: 3` (top).
   - `highestZIndex` is `3`.
2. **User clicks Box 1 (Coral Red)**:
   - Click listener fires on `#box1`.
   - `highestZIndex` becomes `4`.
   - `box1.style.zIndex = 4`.
   - Since `4 > 3`, Box 1 immediately renders in front of Box 2 and Box 3!
3. **User clicks Box 2 (Royal Indigo)**:
   - `highestZIndex` becomes `5`.
   - `box2.style.zIndex = 5`.
   - Box 2 now moves to the very top.
4. **User clicks "Reset Layers"**:
   - `z-index` for Box 1, 2, and 3 are restored to 1, 2, and 3 respectively.
   - `highestZIndex` resets to 3.

Now that you've toured all four programs, test your knowledge with [VIVA-PREP.md](VIVA-PREP.md)!
