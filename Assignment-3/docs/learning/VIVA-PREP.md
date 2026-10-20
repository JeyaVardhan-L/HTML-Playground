# Lab Viva Preparation: 22 High-Yield Questions & Answers

This guide prepares you for your lab examination or viva voce. Every answer is tailored directly to your **Assignment 3** implementation and phrased in clear, beginner-friendly language that you can comfortably speak to an examiner.

---

### Question 1: What is JavaScript, and what role does it play in a web page?
- **Model Answer**: JavaScript is a lightweight, interpreted, client-side programming language. While HTML defines the structure and CSS defines the appearance, JavaScript adds interactivity, logic, data calculation, and dynamic behavior (like validating forms and moving elements) directly in the user's browser.
- **Reference**: `practical-1-form.html`, `practical-2-basics.html`

---

### Question 2: What is the difference between HTML and JavaScript?
- **Model Answer**: HTML is a markup language used to structure content on a page using tags (like headings, inputs, and tables). JavaScript is a programming language that can perform computations, make decisions using `if/else`, respond to user events, and modify the HTML content dynamically after the page has loaded.

---

### Question 3: What is the difference between `let` and `const`?
- **Model Answer**: Both declare block-scoped variables in modern JavaScript. `const` is used for variables whose reference cannot be reassigned (such as DOM element references: `const form = document.getElementById(...)`). `let` is used when the value will change over time (such as counters: `let highestZIndex = 3;` or flags: `let isValid = true;`).
- **Reference**: `practical-1-form.html` (lines 239, 258)

---

### Question 4: What is a data type? What primitive data types exist in JavaScript?
- **Model Answer**: A data type describes the kind of value a variable can store. JavaScript has 7 primitive types. The 5 most common are:
  1. **String**: textual data (e.g. `"John Doe"`).
  2. **Number**: integers and floating-point numbers (e.g. `42`, `3.14`).
  3. **Boolean**: logical `true` or `false`.
  4. **Undefined**: a variable declared but not assigned a value.
  5. **Null**: an intentional absence of any object value.
- **Reference**: `practical-2-basics.html` (lines 301–316)

---

### Question 5: What is an expression in JavaScript?
- **Model Answer**: An expression is any valid unit of code that resolves to a single value. Examples include arithmetic expressions (`15 + 4` which resolves to `19`), comparison expressions (`a > b` which resolves to `true`), and logical expressions (`isValid && hasAge`).
- **Reference**: `practical-2-basics.html` (lines 323–342)

---

### Question 6: What is a function, and why are parameters and return values useful?
- **Model Answer**: A function is a reusable block of code that performs a specific task when called. Parameters allow us to pass inputs into the function, and the `return` statement sends the computed result back to the caller. For example, `calculateCircleArea(radius)` accepts a radius and returns the computed area (`Math.PI * radius * radius`).
- **Reference**: `practical-2-basics.html` (lines 345–355)

---

### Question 7: What are control statements? Give examples from your assignment.
- **Model Answer**: Control statements control the execution flow of a program. They include:
  1. **Conditional Statements (`if / else if / else`)**: Used in `practical-1-form.html` to verify whether fields like age or email meet validation rules.
  2. **Loops (`for` loop)**: Used in `practical-2-basics.html` to generate multiples of 3 repeatedly.
- **Reference**: `practical-1-form.html` (lines 268–322)

---

### Question 8: What is the DOM (Document Object Model)?
- **Model Answer**: The DOM is the browser's in-memory, tree-structured object representation of an HTML document. Every HTML tag becomes a DOM node that JavaScript can select, inspect, and modify using methods like `getElementById` and `querySelector`.

---

### Question 9: What is the difference between `document.getElementById()` and `document.querySelector()`?
- **Model Answer**: `getElementById()` accepts only an element ID without any `#` prefix and returns that single matching element. `querySelector()` accepts any standard CSS selector (e.g. `input[name="gender"]:checked` or `.error-msg`) and returns the first element that matches.
- **Reference**: `practical-1-form.html` (lines 239, 266)

---

### Question 10: How does JavaScript change an HTML element?
- **Model Answer**: JavaScript can change an element in multiple ways:
  1. Updating text content: `element.textContent = "Error message";`
  2. Updating HTML markup: `element.innerHTML = "<li>New Item</li>";`
  3. Modifying CSS styles: `element.style.display = "block";` or `element.style.left = "100px";`
  4. Adding/removing classes: `element.classList.add("dragging");`
- **Reference**: `practical-1-form.html`, `practical-3-drag-drop.html`

---

### Question 11: What is an event and an event listener?
- **Model Answer**: An **event** is an action that takes place in the browser—such as a user clicking a button (`click`), submitting a form (`submit`), typing (`input`), or dragging an image (`dragstart`). An **event listener** is a JavaScript function registered on an element that waits for that event and executes callback code in response.
- **Reference**: `form.addEventListener("submit", function(event) { ... });`

---

### Question 12: Why is `event.preventDefault()` essential when handling form submissions?
- **Model Answer**: By default, submitting an HTML form sends an HTTP request and reloads the entire web page. In client-side single-page applications, we want JavaScript to validate inputs and display messages without losing the user's data or resetting the page. Calling `event.preventDefault()` stops the default reload.
- **Reference**: `practical-1-form.html` (line 253)

---

### Question 13: What is a JavaScript object?
- **Model Answer**: An object is a collection of related key-value pairs. Keys that hold data values are called **properties**, and keys that hold functions are called **methods**. In `practical-2-basics.html`, we created a `student` object with properties like `name` and `marks`, and a method `calculateAverage()`.
- **Reference**: `practical-2-basics.html` (lines 384–403)

---

### Question 14: What is the purpose of the `this` keyword inside an object method?
- **Model Answer**: Inside an object method, `this` refers to the object itself. In `this.marks.length`, `this` references the `student` object, allowing the method to access the student's own marks property.
- **Reference**: `practical-2-basics.html` (line 392)

---

### Question 15: What is DHTML (Dynamic HTML)?
- **Model Answer**: DHTML is the combination of HTML, CSS, and JavaScript working together to dynamically modify a page's content, styling, or positioning in real time after it has loaded, without requiring a server roundtrip. For example, dragging an image to new coordinates or clicking a card to change its `z-index` are classic DHTML techniques.
- **Reference**: `practical-3-drag-drop.html`, `practical-4-stacking.html`

---

### Question 16: How does CSS `z-index` work, and why must elements be positioned?
- **Model Answer**: `z-index` specifies the visual stack order (depth along the z-axis) of overlapping HTML elements. Elements with a higher `z-index` render on top of elements with lower numbers. It **only** works on positioned elements (elements with `position: absolute`, `relative`, or `fixed`); it has no effect on default `position: static` elements.
- **Reference**: `practical-4-stacking.html` (lines 80–135)

---

### Question 17: How did you implement dynamic stacking in Practical 4?
- **Model Answer**: I initialized a counter `let highestZIndex = 3;`. I added a `click` event listener to each box. When any box is clicked, JavaScript increments the counter (`highestZIndex++`) and applies it to that box's inline style (`this.style.zIndex = highestZIndex;`). This guarantees that the most recently clicked box always sits on top.
- **Reference**: `practical-4-stacking.html` (lines 245–257)

---

### Question 18: What are the main events in HTML5 Drag and Drop?
- **Model Answer**:
  1. `dragstart`: Fires on the draggable element when the user starts dragging.
  2. `dragover`: Fires continuously on the drop target as the item hovers over it. **Must call `event.preventDefault()` to allow dropping!**
  3. `drop`: Fires on the drop target when the user releases the mouse.
  4. `dragend`: Fires on the dragged element when dragging finishes.
- **Reference**: `practical-3-drag-drop.html` (lines 240–310)

---

### Question 19: What does `draggable="true"` do on an image?
- **Model Answer**: `draggable="true"` is an HTML5 attribute that tells the browser that this element is permitted to be dragged by the user using the native HTML5 drag-and-drop system.
- **Reference**: `practical-3-drag-drop.html` (line 197)

---

### Question 20: How does error handling work with `try`, `throw`, and `catch`?
- **Model Answer**:
  - Code that might cause an error is placed inside the `try { ... }` block.
  - If something invalid occurs (like dividing by zero), we `throw new Error(...)`.
  - The `catch (err) { ... }` block catches the error and displays a safe message without crashing the script.
  - The `finally { ... }` block runs in all situations, whether an error occurred or not.
- **Reference**: `practical-2-basics.html` (lines 450–472)

---

### Question 21: How do you format a date using JavaScript's `Date` object?
- **Model Answer**: We create an instance with `const now = new Date();`. We can extract formatted strings using `.toDateString()` (calendar date), `.toLocaleTimeString()` (time), and `.getFullYear()` (4-digit year).
- **Reference**: `practical-2-basics.html` (lines 407–417)

---

### Question 22: What is the purpose of the `.trim()` string method in form validation?
- **Model Answer**: `.trim()` removes whitespace characters (spaces, tabs, newlines) from both the beginning and the end of a string. In form validation, it prevents a user from bypassing a required field by simply typing empty spaces.
- **Reference**: `practical-1-form.html` (line 260)

Now practice the hands-on modifications in [HANDS-ON-EXERCISES.md](HANDS-ON-EXERCISES.md)!
