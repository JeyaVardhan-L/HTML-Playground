# JavaScript From Zero: Beginner's Theory Guide

This guide teaches the complete set of JavaScript concepts covered in **Assignment 3**. Every topic includes a plain-English explanation, a small code snippet, an everyday analogy, and a pointer to where it appears in our assignment code.

---

## 1. Variables: `const` and `let`

A **variable** is a named storage container in computer memory where you can keep data for later use.

```javascript
const pi = 3.14159;  // Cannot be reassigned
let counter = 1;     // Can be updated later
counter = counter + 1;
```

- **`const` (Constant)**: Use this whenever the value or element reference should never be reassigned.
  - *Where used in our code*: Storing DOM element references in `practical-1-form.html` (`const form = document.getElementById("registrationForm");`).
- **`let`**: Use this when the value will change over time (e.g. counters, loop iterators, or flags).
  - *Where used in our code*: `let isValid = true;` in `practical-1-form.html`, `let highestZIndex = 3;` in `practical-4-stacking.html`.
- **Analogy**: A `const` variable is like writing with permanent ink on a labeled jar; a `let` variable is like writing with a dry-erase marker so you can change what is written on it later.

---

## 2. Primitive Data Types

JavaScript categorizes data into distinct **types**. A "primitive" is a single, immutable raw value:

| Data Type | Description | Example | Where in Our Code |
| :--- | :--- | :--- | :--- |
| **String** | Text characters enclosed in quotes (`"` or `'` or backticks `` ` ``). | `"John Doe"`, `"user@example.com"` | `fullName = document.getElementById("fullName").value.trim()` in Practical 1 |
| **Number** | Numeric values (integers or decimals). | `42`, `3.14`, `-10` | `ageNumber = Number(ageValue)` in Practical 1; `Math.PI` in Practical 2 |
| **Boolean** | Logical truth value: either `true` or `false`. | `true`, `false` | `let isValid = true;` in Practical 1 |
| **Undefined** | A variable that has been declared but not assigned any value yet. | `let x;` (`x` is `undefined`) | Tested in Practical 2 data types table |
| **Null** | An intentional representation of "no value" or "empty". | `null` | Historical quirk: `typeof null` returns `"object"` in Practical 2 |

### Type Checking with `typeof`
In JavaScript, the `typeof` operator returns a string stating the data type:
```javascript
typeof "Frontier AI" // returns "string"
typeof 42            // returns "number"
typeof true          // returns "boolean"
```
*Where in our code*: The data types table in `practical-2-basics.html` (lines 301–316).

---

## 3. Operators & Expressions

An **expression** is any valid piece of JavaScript code that the browser resolves into a single value.

### Arithmetic Operators
Perform mathematical calculations:
- `+` (Addition), `-` (Subtraction), `*` (Multiplication), `/` (Division), `%` (Modulus / Remainder).
```javascript
let remainder = 15 % 4; // returns 3 (15 divided by 4 is 3 with remainder 3)
```
*Where in our code*: `practical-2-basics.html` (Section 2).

### Comparison Operators
Compare two values and produce a boolean (`true` or `false`):
- `===` (Strict equality: checks both value and type)
- `!==` (Strict inequality)
- `>` (Greater than), `<` (Less than), `>=` (Greater than or equal), `<=` (Less than or equal)
```javascript
18 >= 18   // true
"18" === 18 // false (different types: string vs number)
```
*Where in our code*: `if (ageNumber < 18 || ageNumber > 100)` in `practical-1-form.html`.

### Logical Operators
Combine multiple boolean conditions:
- `&&` (Logical AND): Returns `true` only if **both** sides are true.
- `||` (Logical OR): Returns `true` if **either** side is true.
- `!` (Logical NOT): Inverts a boolean (`!true` is `false`).
```javascript
if (age >= 18 && hasID === true) { ... }
```
*Where in our code*: `practical-1-form.html` (lines 280, 290).

---

## 4. Functions: Parameters, Return Values & Invocation

A **function** is a packaged, reusable set of instructions that performs a specific task.

```javascript
// Function Declaration
function calculateCircleArea(radius) {
  // 'radius' is the parameter (input)
  const area = Math.PI * radius * radius;
  return area.toFixed(2); // 'return' sends the result back to whoever called it
}

// Function Invocation (Call)
const myResult = calculateCircleArea(5); // myResult holds "78.54"
```

### Components of a Function:
1. **Name**: `calculateCircleArea` identifies the function.
2. **Parameters**: Variables listed inside parentheses in the declaration (`radius`). They act as placeholders for incoming values.
3. **Arguments**: The real values passed in during invocation (`5`).
4. **`return` statement**: Halts function execution and hands a value back to the caller. If omitted, the function returns `undefined`.
- **Analogy**: A function is like a kitchen blender. The parameters are the ingredients you toss in the top, the code inside is the blades spinning, and the return value is the smoothie poured out the bottom.
- *Where in our code*: `setError(elementId, message)` in Practical 1; `calculateCircleArea(radius)` and `getGrade(score)` in Practical 2.

---

## 5. Control Statements: `if/else` Decisions and `for` Loops

Control statements dictate the **flow of execution** through your program.

### `if / else if / else`
Executes different blocks of code depending on whether conditions evaluate to `true` or `false`:
```javascript
function getGrade(score) {
  if (score >= 90) {
    return "Grade A";
  } else if (score >= 75) {
    return "Grade B";
  } else {
    return "Grade F";
  }
}
```
*Where in our code*: Form validation in `practical-1-form.html` (lines 268–322) and grade decision in `practical-2-basics.html` (lines 351–362).

### The `for` Loop
Repeats a block of code a specific number of times:
```javascript
// Syntax: for (initialization; condition; increment)
for (let i = 1; i <= 5; i++) {
  console.log("Count: " + i);
}
```
- Step 1: `let i = 1` runs once at the very start.
- Step 2: Checks `i <= 5`. If true, the code inside the loop executes.
- Step 3: `i++` increments `i` by 1.
- Step 4: Repeats until the condition becomes false.
*Where in our code*: Loop demonstration generating multiples of 3 in `practical-2-basics.html` (lines 375–379).

---

## 6. JavaScript Objects & Methods

An **object** is a container that stores related data in **key-value pairs** (called properties) and functions (called methods):

```javascript
const student = {
  // Properties (State)
  name: "Jey",
  rollNo: "9057",
  marks: [85, 90, 88],

  // Method (Behavior)
  calculateAverage: function () {
    let total = 0;
    for (let i = 0; i < this.marks.length; i++) {
      total += this.marks[i];
    }
    return (total / this.marks.length).toFixed(1);
  }
};

// Accessing properties:
console.log(student.name); // "Jey"

// Invoking a method:
console.log(student.calculateAverage()); // "87.7"
```

### The `this` Keyword
Inside an object method, `this` refers to the **object itself**. In `this.marks`, `this` points to `student`, allowing the method to access the student's own marks array.
- *Where in our code*: `practical-2-basics.html` (Section 5, lines 384–403).

---

## 7. DOM Methods: Selecting & Modifying Elements

The **DOM (Document Object Model)** is the browser's internal representation of the HTML document. When JavaScript interacts with a webpage, it does so through DOM methods:

### Selecting Elements:
- `document.getElementById("idName")`: Returns the single element with that unique ID.
- `document.querySelector(".className")`: Returns the *first* element matching a CSS selector.
- `document.querySelectorAll(".box")`: Returns a *NodeList* (an array-like collection) of all matching elements.

### Modifying Elements:
- `element.textContent = "New text"`: Safely replaces the plain text inside an element.
- `element.innerHTML = "<strong>Bold</strong>"`: Inserts HTML markup inside an element.
- `element.style.color = "red"`: Changes CSS properties directly on the element.
- `element.classList.add("active")` / `remove("active")`: Toggles CSS classes.
*Where in our code*: Used across all four practicals.

---

## 8. Events, Event Listeners & `event.preventDefault()`

An **event** is an action detected by the browser—such as a click, a keystroke, form submission, or mouse drag.

### Adding an Event Listener:
```javascript
// Target element.addEventListener("event_type", callback_function)
button.addEventListener("click", function (event) {
  alert("Button was clicked!");
});
```

### `event.preventDefault()`
Normally, submitting a form causes the browser to reload the page and send an HTTP request. Calling `event.preventDefault()` stops this default behavior so your JavaScript code can validate inputs and update the screen without losing state:
```javascript
form.addEventListener("submit", function (event) {
  event.preventDefault(); // HALTS page reload!
  // Our validation runs here...
});
```
*Where in our code*: `practical-1-form.html` (line 253), `practical-3-drag-drop.html` (line 270).

---

## 9. Built-in Objects: `Date`, String Methods & Error Handling

### The `Date` Object
JavaScript provides a built-in `Date` object to work with calendar dates and timestamps:
```javascript
const now = new Date();
now.toDateString();        // e.g. "Tue Oct 20 2026"
now.toLocaleTimeString();  // e.g. "3:45:12 PM"
now.getFullYear();         // e.g. 2026
```
*Where in our code*: `practical-2-basics.html` (Section 6) and `practical-3-drag-drop.html` (timestamped event log).

### Common String Methods
Strings have built-in helper methods:
- `.toUpperCase()`: Converts text to all capital letters (`"hello"` → `"HELLO"`).
- `.toLowerCase()`: Converts text to all lowercase letters.
- `.trim()`: Strips whitespace from both ends (`"  John  "` → `"John"`).
- `.includes("word")`: Returns `true` if the substring exists inside the string.
*Where in our code*: `practical-2-basics.html` (Section 7) and `practical-1-form.html` (trimming input values).

### Error Handling: `try / throw / catch / finally`
Error handling ensures that runtime errors do not crash your script:
```javascript
function divide(a, b) {
  if (b === 0) {
    throw new Error("Cannot divide by zero!"); // Throws an error object
  }
  return a / b;
}

try {
  // Code that might fail
  const answer = divide(10, 0);
  console.log(answer);
} catch (err) {
  // Runs ONLY if an error occurred in the try block
  console.error("Caught:", err.message);
} finally {
  // Runs ALWAYS, regardless of whether there was an error
  console.log("Calculation attempt finished.");
}
```
*Where in our code*: `practical-2-basics.html` (Section 8, lines 442–472).

---

## 10. DHTML (Dynamic HTML)

**DHTML** is not a separate programming language. It is the combination of **HTML + CSS + JavaScript** working together to create web pages that dynamically alter their content, appearance, and position after the page has finished loading.

In our practicals, DHTML is demonstrated when:
1. **Practical 1**: Revealing the green `#successCard` and injecting student data dynamically.
2. **Practical 3**: Dynamically setting `dragImage.style.left` and `dragImage.style.top` in response to mouse drop coordinates.
3. **Practical 4**: Dynamically modifying `box.style.zIndex` when clicked to change visual depth.

Now that you understand the theory, explore [CODE-EXPLANATION.md](CODE-EXPLANATION.md) for a line-by-line tour of each practical!
