# Code Explanation: Deep Dive into All Six Practicals

This document provides a line-by-line and block-by-block technical walkthrough of every file and component in **Assignment 4**.

---

## Practical 1 — Express Server and Browser Fetch (`express-fetch/`)

### 1. Purpose
Demonstrates how a backend Node.js + Express web server listens on a local port, serves static HTML, and responds to an asynchronous client-side HTTP `GET` fetch request with JSON data.

### 2. Backend Code Walkthrough (`server.js`)
```javascript
const express = require("express");
const path = require("path");

const app = express();
const PORT = process.env.PORT || 3000;
```
- **Line 1–2**: Imports the `express` library and Node.js built-in `path` module.
- **Line 4–5**: Initializes the Express application instance (`app`) and sets the port to `3000` (or the environment variable `PORT` if specified).

```javascript
app.use(express.static(path.join(__dirname, "public")));
```
- **Line 8**: Middleware that serves all static assets (HTML, CSS, JS) from the `public` directory. When a user requests `http://localhost:3000/`, Express serves `public/index.html`.

```javascript
const studentData = {
  id: 9057,
  name: "Jey",
  rollNo: "9057",
  branch: "Computer Science & Engineering",
  year: "3rd Year (Semester 5)",
  university: "GITAM University",
  cgpa: 9.2,
  status: "Active Full-Time Student"
};
```
- **Line 11–20**: A hardcoded JavaScript object acting as our data store (simulating database records).

```javascript
app.get("/api/student", (req, res) => {
  const timestamp = new Date().toLocaleTimeString();
  console.log(`[EXPRESS SERVER ${timestamp}] Received GET request for /api/student`);
  res.json(studentData);
});
```
- **Line 23–27**: Defines the API route `GET /api/student`.
  - When invoked, it prints a message to the server's terminal with the current time.
  - `res.json(studentData)` automatically serializes the JavaScript object into JSON format, sets HTTP status code `200`, and attaches the header `Content-Type: application/json`.

```javascript
app.listen(PORT, () => {
  console.log(`🚀 Express Server is running on http://localhost:${PORT}`);
});
```
- **Line 35–41**: Binds the server to port 3000 and begins listening for network requests.

### 3. Frontend Client Code Walkthrough (`public/index.html`)
```javascript
async function fetchStudentData() {
  errorBox.style.display = "none";
  studentContainer.style.display = "none";
  loadingIndicator.style.display = "block";
  fetchBtn.disabled = true;

  try {
    const response = await fetch("/api/student");
    if (!response.ok) {
      throw new Error(`Server returned HTTP status ${response.status}`);
    }
    const data = await response.json();

    studentName.textContent = data.name;
    studentRoll.textContent = data.rollNo;
    studentBranch.textContent = data.branch;
    studentYear.textContent = data.year;
    studentUniversity.textContent = data.university;
    studentStatus.textContent = data.status;

    studentContainer.style.display = "block";
  } catch (error) {
    errorBox.textContent = `⚠ Failed to fetch student data: ${error.message}`;
    errorBox.style.display = "block";
  } finally {
    loadingIndicator.style.display = "none";
    fetchBtn.disabled = false;
  }
}
```
- **`async/await`**: Pauses inside `fetchStudentData()` while waiting for the network response, without freezing the browser tab.
- **`response.json()`**: Reads the stream and parses raw JSON text into a usable JavaScript object.
- **`catch (error)`**: Gracefully catches network errors (e.g. if the server is stopped) and displays a clean error banner in the DOM.

### 4. What would happen if you modified a line?
- If you changed `res.json(studentData)` to `res.send("Hello")` in `server.js`:
  - `response.json()` on the client would throw a `SyntaxError: Unexpected token 'H'` because `"Hello"` is not valid JSON!

---

## Practical 2 — React State: Increment and Decrement (`StateCounter.jsx`)

### 1. Purpose
Demonstrates how local state is created using the `useState` hook and how state updates trigger immediate UI re-renders.

### 2. Code Walkthrough
```jsx
function StateCounter() {
  const [count, setCount] = useState(0);

  const handleIncrement = () => setCount(count + 1);
  const handleDecrement = () => setCount(count - 1);
  const handleReset = () => setCount(0);

  return (
    <div className="practical-card">
      <div className="counter-display">{count}</div>
      <div className="counter-controls">
        <button onClick={handleDecrement}>− Decrement</button>
        <button onClick={handleReset}>Reset (0)</button>
        <button onClick={handleIncrement}>+ Increment</button>
      </div>
    </div>
  );
}
```
- **`useState(0)`**: Initializes `count` to `0`. Returns a two-item array: the current value (`count`) and the updater function (`setCount`).
- **`onClick={handleIncrement}`**: Passes a function reference. When the user clicks the button, React invokes `setCount(count + 1)`.

### 3. Step-by-Step Interaction Trace
1. User clicks the **"+ Increment"** button.
2. `handleIncrement` is called → calls `setCount(0 + 1)`.
3. React registers that `count` has changed from `0` to `1`.
4. React calls `StateCounter()` again (re-render).
5. The JSX returns with `{count}` resolving to `1`.
6. React updates the virtual DOM, finds the difference, and updates only the `<div className="counter-display">` on the real screen.

---

## Practical 3 — React Class Component (`ClassStudent.jsx`)

### 1. Purpose
Demonstrates the structure of an ES6 class component inheriting from `React.Component` and using constructor state and the `render()` method.

### 2. Code Walkthrough
```jsx
class ClassStudent extends Component {
  constructor(props) {
    super(props);
    this.state = {
      studentName: "Jey (Roll 9057)",
      branch: "Computer Science & Engineering",
      semester: "Semester 5 (3rd Year)",
      bio: "Undergraduate student passionate about cloud systems..."
    };
  }

  render() {
    return (
      <div className="student-badge-card">
        <h3>{this.state.studentName}</h3>
        <p>{this.state.branch}</p>
        <p>{this.state.semester}</p>
        <p>{this.state.bio}</p>
      </div>
    );
  }
}
```
- **`super(props)`**: Calls the parent constructor in `React.Component`, initializing `this` properly.
- **`this.state = { ... }`**: In class components, state must be defined as an object in the constructor.
- **`render()`**: Required lifecycle method in every class component. React calls this to know what JSX to paint on screen.

### 3. What would happen if `render()` was omitted?
- React would throw a fatal error: `Error: ClassStudent(...): Must contain a "render" method on the component instance.`

---

## Practical 4 — React Props (`StudentProps.jsx`)

### 1. Purpose
Demonstrates parent-to-child data flow using props and rendering dynamic lists with `.map()`.

### 2. Code Walkthrough

#### Child Component (`StudentCard`):
```jsx
function StudentCard({ name, branch, rollNo, year }) {
  return (
    <div className="student-badge-card">
      <h3>{name}</h3>
      <p>Roll: {rollNo}</p>
      <p>Branch: {branch}</p>
      <p>Year: {year}</p>
    </div>
  );
}
```
- Uses **parameter destructuring** `{ name, branch, rollNo, year }` to unpack properties sent by the parent.
- Props are **read-only**: `StudentCard` cannot modify `name` or `branch`.

#### Parent Component (`StudentProps`):
```jsx
function StudentProps() {
  const studentsList = [
    { id: 1, name: "Jey", rollNo: "9057", branch: "CSE", year: "3rd Year" },
    { id: 2, name: "Aarav Sharma", rollNo: "9012", branch: "ECE", year: "3rd Year" },
    { id: 3, name: "Priya Nair", rollNo: "9084", branch: "AI & DS", year: "2nd Year" }
  ];

  return (
    <div className="student-list-grid">
      {studentsList.map((student) => (
        <StudentCard
          key={student.id}
          name={student.name}
          rollNo={student.rollNo}
          branch={student.branch}
          year={student.year}
        />
      ))}
    </div>
  );
}
```
- `studentsList.map(...)`: Loops over each student object in the array and returns a configured `<StudentCard />` component instance.
- `key={student.id}`: Provides a unique identifier for React's reconciliation engine.

---

## Practical 5 — React Hooks: At Least Three (`HooksDemo.jsx`)

### 1. Purpose
Demonstrates three distinct React hooks (`useState`, `useRef`, and `useEffect`) working together cohesively in a single application.

### 2. Code Walkthrough
```jsx
function HooksDemo() {
  // Hook 1: useState (maintains counter and input string)
  const [clicks, setClicks] = useState(0);
  const [inputText, setInputText] = useState("React is declarative!");

  // Hook 2: useRef (stores reference to the real input DOM node)
  const inputRef = useRef(null);

  // Hook 3: useEffect (synchronizes tab title with clicks count)
  useEffect(() => {
    const originalTitle = document.title;
    document.title = `Clicked ${clicks} times — Hooks Demo`;

    return () => {
      document.title = originalTitle; // cleanup
    };
  }, [clicks]);

  const handleFocusClick = () => {
    if (inputRef.current) {
      inputRef.current.focus();
      inputRef.current.select();
    }
  };
```
- **`useState`**: Provides reactive state for the counter and live text field.
- **`useRef(null)`**: Holds a direct reference to the `<input ref={inputRef} />` element. `inputRef.current.focus()` executes imperatively without causing any component re-render.
- **`useEffect`**: Synchronizes the browser window's `document.title` whenever `clicks` changes. The returned arrow function is the **cleanup function**.

---

## Practical 6 — React Function Component (`FunctionStudent.jsx`)

### 1. Purpose
Demonstrates modern standard React development: writing a clean JavaScript function that accepts props and returns JSX directly.

### 2. Code Walkthrough
```jsx
function FunctionStudent() {
  const student = {
    name: "Jey",
    rollNo: "9057",
    branch: "Computer Science & Engineering",
    yearOfStudy: "3rd Year (B.Tech)",
    college: "GITAM School of Technology",
    specialization: "Web Application Frameworks & AI"
  };

  return (
    <div className="student-badge-card">
      <h3>🧑‍💻 Student Record (Function Component)</h3>
      <p>Name: {student.name}</p>
      <p>Roll: {student.rollNo}</p>
      <p>Branch: {student.branch}</p>
      <p>Year: {student.yearOfStudy}</p>
      <p>College: {student.college}</p>
    </div>
  );
}
```
- Demonstrates how simple and clean function components are compared to class components. No constructors, no `this`, and no `render()` wrapper required.

Now practice oral exam scenarios in [VIVA-PREP.md](VIVA-PREP.md)!
