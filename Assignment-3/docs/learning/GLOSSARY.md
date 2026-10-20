# Technical Glossary: JavaScript & DOM Terms Explained

A quick-reference dictionary of technical web terms used in **Assignment 3**. Each term is defined in 1–2 simple sentences with code examples.

---

## 1. Core JavaScript Terms

### Variable
A named storage container in computer memory that holds a value for later use.  
*Example*: `const age = 21;` or `let isValid = true;`.

### Primitive Data Type
A basic, built-in data type in JavaScript that represents a single, raw value.  
*Example*: String, Number, Boolean, Undefined, and Null.

### Expression
Any valid unit of JavaScript code that the browser resolves into a single value.  
*Example*: `15 + 4` (evaluates to `19`), or `age >= 18` (evaluates to `true`).

### Operator
A special symbol that performs an operation on one or more values (operands).  
*Example*: Arithmetic (`+`, `-`, `*`, `/`, `%`), Comparison (`===`, `!==`, `>`, `<`), and Logical (`&&`, `||`, `!`).

### Function
A reusable block of statements designed to perform a particular task when invoked.  
*Example*: `function calculateCircleArea(radius) { return Math.PI * radius * radius; }`.

### Parameter
A variable listed inside the parentheses of a function definition that acts as a placeholder for incoming data.  
*Example*: `radius` in `function calculateCircleArea(radius)`.

### Argument
The actual real value passed into a function when it is invoked.  
*Example*: `5` in `calculateCircleArea(5)`.

### Return Value
The value sent back to the caller when a function executes its `return` statement.  
*Example*: `return area.toFixed(2);`.

### Conditional Statement (`if / else`)
A control structure that makes decisions by executing different blocks of code depending on whether a condition is `true` or `false`.  
*Example*: `if (age < 18) { setError("Age must be at least 18"); }`.

### Loop (`for` / `while`)
A control structure that repeats a block of code multiple times until a condition becomes false.  
*Example*: `for (let i = 1; i <= 5; i++) { ... }`.

---

## 2. Objects & Built-Ins

### Object
A compound data structure that stores related state (properties) and actions (methods) in key-value pairs.  
*Example*: `const student = { name: "Jey", rollNo: "9057" };`.

### Property
A named variable attached to an object holding a specific value.  
*Example*: `student.name` evaluates to `"Jey"`.

### Method
A function that is defined as a property inside an object.  
*Example*: `student.calculateAverage()`.

### `this` Keyword
A special identifier that refers to the current object executing the method.  
*Example*: `this.marks` inside `student.calculateAverage()` refers to the student's own marks property.

### `Date` Object
A built-in JavaScript object used to work with calendar dates, times, and timestamps.  
*Example*: `const now = new Date();` and `now.toDateString();`.

### String Method
A built-in helper function attached to string values.  
*Example*: `"hello".toUpperCase()` returns `"HELLO"`; `"  text  ".trim()` returns `"text"`.

### Error Handling (`try / catch / finally`)
A construct used to catch runtime exceptions safely without crashing the entire script.  
*Example*: `try { divide(10, 0); } catch (err) { alert(err.message); }`.

---

## 3. DOM & Browser Events

### DOM (Document Object Model)
The browser's in-memory, tree-structured object representation of an HTML document that JavaScript can inspect and modify.  
*Example*: Every HTML tag (`<form>`, `<div>`, `<input>`) becomes a node in the DOM tree.

### `document.getElementById()`
A DOM method that finds and returns the single element matching the provided ID string.  
*Example*: `document.getElementById("fullName")`.

### `document.querySelector()`
A DOM method that returns the first element matching a specified CSS selector.  
*Example*: `document.querySelector('input[name="gender"]:checked')`.

### `document.querySelectorAll()`
A DOM method that returns a collection (NodeList) of all elements matching a CSS selector.  
*Example*: `document.querySelectorAll(".box")`.

### `textContent`
A DOM property that reads or updates the plain, unformatted text inside an HTML element.  
*Example*: `errorSpan.textContent = "Name is required.";`.

### `innerHTML`
A DOM property that reads or sets the HTML markup content inside an element.  
*Example*: `summaryList.innerHTML = "<li>Name: John</li>";`.

### Event
A signal emitted by the browser when an interaction occurs (such as a click, submit, keystroke, or drag).  
*Example*: `"click"`, `"submit"`, `"dragstart"`, `"drop"`.

### Event Listener
A method that registers a callback function to run whenever a specific event is detected on an element.  
*Example*: `button.addEventListener("click", function() { ... })`.

### `event.preventDefault()`
A method that stops the browser's default behavior for an event (such as preventing a page reload during form submission).  
*Example*: `event.preventDefault()` inside a form submit handler.

---

## 4. DHTML & CSS Manipulation

### DHTML (Dynamic HTML)
The collective term for using HTML, CSS, and JavaScript together to dynamically alter page content, styles, and positions after loading.  
*Example*: Dragging an image or clicking a card to change its `z-index`.

### `z-index`
A CSS property that controls the 3D stacking order (depth along the z-axis) of overlapping positioned elements.  
*Example*: `element.style.zIndex = 10;` brings the element in front of an element with `z-index: 2`.

### `draggable="true"`
An HTML5 attribute that enables an element to be picked up and moved using the native drag-and-drop system.  
*Example*: `<img src="assets/star.svg" draggable="true">`.

### `dataTransfer`
The browser object used in drag-and-drop events to hold data being dragged and configure drop effects.  
*Example*: `event.dataTransfer.setData("text/plain", dragImage.id)`.
