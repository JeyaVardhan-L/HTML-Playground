# Viva Voce & Practical Exam Preparation Guide

This guide contains **30 curated viva questions** commonly asked by external and internal examiners for Web Application Frameworks (WAF) lab practicals covering **Node.js, Express, `fetch()`, and React**.

Every answer matches our actual Assignment 4 codebase and is formulated in conversational, spoken English so you can explain it aloud confidently during your examination.

---

## Table of Contents
1. [Category 1: Client-Server Architecture & Express (Q1–Q6)](#category-1-client-server-architecture--express)
2. [Category 2: HTTP, JSON, and `fetch()` (Q7–Q11)](#category-2-http-json-and-fetch)
3. [Category 3: React Fundamentals & JSX (Q12–Q15)](#category-3-react-fundamentals--jsx)
4. [Category 4: Function vs. Class Components (Q16–Q18)](#category-4-function-vs-class-components)
5. [Category 5: Props vs. State (Q19–Q21)](#category-5-props-vs-state)
6. [Category 6: React Hooks (`useState`, `useRef`, `useEffect`) (Q22–Q26)](#category-6-react-hooks)
7. [Category 7: Project Setup, Ports, and Debugging (Q27–Q30)](#category-7-project-setup-ports-and-debugging)

---

## Category 1: Client-Server Architecture & Express

### Q1: What is Express.js, and why do we use it in Practical 1?
> **Answer:**  
> "Express is a fast, minimalist web framework for Node.js. In Practical 1, we use Express to create a local HTTP server on port 3000. It handles two jobs: first, serving our static frontend files (`index.html`) using `express.static('public')`; and second, providing an API route (`GET /api/student`) that returns structured JSON data when requested by the browser."

### Q2: What is the difference between client-side code and server-side code in Practical 1?
> **Answer:**  
> "Server-side code is written in `server.js` and runs on our local machine inside the Node.js runtime. It has access to our computer's ports, file system, and console. Client-side code is written in `public/index.html` inside `<script>` tags and runs inside the user's web browser (V8 engine). The browser client cannot directly touch the server's variables; they only communicate over the network using HTTP requests and responses."

### Q3: What is middleware in Express, and which middleware did you use?
> **Answer:**  
> "Middleware is a function in Express that executes between receiving an incoming HTTP request and sending the final response. In `server.js`, we used `app.use(express.static(path.join(__dirname, 'public')))`. This built-in static middleware automatically looks inside the `public/` directory and delivers `index.html` whenever a user opens `http://localhost:3000`."

### Q4: Why does `server.js` log to the terminal, and why can't the user see that in their browser?
> **Answer:**  
> "In `server.js`, `console.log(...)` executes in the Node process running in our command prompt or terminal window. Because it runs on the backend server, its standard output is directed to that terminal. The browser only sees what the server explicitly sends back in the HTTP response body (`res.json(...)`)."

### Q5: What does `app.listen(PORT, callback)` do?
> **Answer:**  
> "It binds the Express application to a specific network port (port 3000 in our project) and starts listening for incoming TCP/HTTP connection requests. Once the port is successfully bound, Express invokes the callback function to print our startup confirmation message in the terminal."

### Q6: Why did you keep student data hardcoded in `server.js` rather than in a database?
> **Answer:**  
> "For this laboratory practical, the objective is to understand the HTTP client-server request-response lifecycle and asynchronous `fetch()`. Hardcoding a JavaScript object directly in `server.js` keeps the project lightweight, dependency-free, zero-config, and instantly runnable locally on any computer without needing database credentials."

---

## Category 2: HTTP, JSON, and `fetch()`

### Q7: What is an API endpoint, and what does `GET /api/student` represent?
> **Answer:**  
> "An API endpoint is a specific URL path exposed by a web server where clients can access a specific service or resource. In our project, `GET /api/student` specifies an HTTP `GET` method targeting the path `/api/student`. When triggered, it executes our route handler in `server.js` and returns the student record."

### Q8: Why are the initial HTML page load and the student data fetch two separate requests?
> **Answer:**  
> "When the user navigates to `http://localhost:3000`, the browser makes Request 1 for the HTML document. That page contains layout and buttons, but no student information. Only when the user clicks 'Fetch Data' does JavaScript execute `fetch('/api/student')` as Request 2. This is the core concept of Single Page Applications (SPAs) and modern AJAX: loading the interface first, and asynchronously fetching data on demand without reloading the entire page."

### Q9: What is JSON, and how is it used in Practical 1?
> **Answer:**  
> "JSON stands for JavaScript Object Notation. It is a lightweight, human-readable text format used for data interchange across web applications. In `server.js`, `res.json(studentData)` serializes our JavaScript object into a JSON string and sets the `Content-Type: application/json` header. In the browser, `await response.json()` parses that JSON string back into a usable JavaScript object."

### Q10: How does `async/await` and `try/catch` work in your `fetchData()` function?
> **Answer:**  
> "`async` designates our function as asynchronous, allowing us to use `await` to pause execution until a Promise resolves without freezing the browser UI. We first `await fetch('/api/student')` to get the HTTP response, and then `await response.json()` to parse the payload. We wrap this in a `try/catch` block so if the server is offline or the network fails, execution immediately jumps to `catch (error)`, allowing us to display a friendly error message to the student instead of crashing."

### Q11: What does `response.ok` check in the fetch handler?
> **Answer:**  
> "`fetch()` only rejects its Promise if there is a network-level failure (such as the server being completely down). If the server returns an HTTP error code like 404 Not Found or 500 Internal Server Error, `fetch()` still resolves. Checking `if (!response.ok)` allows us to detect status codes outside the 200–299 range and manually throw an error into our `catch` block."

---

## Category 3: React Fundamentals & JSX

### Q12: What is React, and what problem does it solve?
> **Answer:**  
> "React is an open-source JavaScript library developed by Meta for building interactive user interfaces. Instead of manually finding DOM elements using `document.getElementById()` and updating their `innerText` whenever data changes, React allows us to declare our UI as a function of state. When state changes, React automatically recalculates and updates only the necessary parts of the real DOM using its Virtual DOM diffing engine."

### Q13: What is JSX, and can browsers execute JSX directly?
> **Answer:**  
> "JSX stands for JavaScript XML. It is a syntax extension for JavaScript that allows us to write HTML-like markup directly inside JavaScript files. Browsers cannot execute JSX directly. During build or development, tools like Vite and Babel compile JSX tags into standard JavaScript `React.createElement()` function calls."

### Q14: What is the Virtual DOM in React?
> **Answer:**  
> "The Virtual DOM is a lightweight, in-memory representation of the real DOM maintained by React. When a component's state or props change, React creates a new Virtual DOM tree, compares it with the previous one (a process called reconciliation or diffing), and calculates the minimal batch of updates needed on the actual browser DOM. This avoids expensive full-page reflows and improves performance."

### Q15: What is the purpose of `src/main.jsx` and `ReactDOM.createRoot`?
> **Answer:**  
> "`main.jsx` is the entry point of our React application. It finds the `<div id="root"></div>` container inside `index.html`, calls `ReactDOM.createRoot()`, and renders our root component `<App />` inside it, mounting the entire React application into the browser page."

---

## Category 4: Function vs. Class Components

### Q16: What is a Class Component in React, as shown in Practical 3?
> **Answer:**  
> "A Class Component is an ES6 class that extends `React.Component`. It must define a `render()` method that returns JSX. In our `ClassStudent.jsx`, the component maintains its data using `this.state` in the constructor, and reads properties using `this.state.studentName`. It represents the legacy, traditional way of writing stateful React components before React 16.8."

### Q17: What is a Function Component in React, as shown in Practical 6?
> **Answer:**  
> "A Function Component is a plain JavaScript function that receives props as an optional parameter and returns JSX. In `FunctionStudent.jsx`, we wrote `function FunctionStudent() { return (...) }`. Modern React almost exclusively uses function components because they are shorter, easier to test, have no `this` binding confusion, and can use React Hooks."

### Q18: What are the main differences between Function and Class components?
> **Answer:**  
> "First, syntax: function components are plain functions returning JSX, whereas class components use ES6 `class ... extends Component` with a required `render()` method.  
> Second, state handling: class components initialize `this.state` in a constructor and call `this.setState()`, whereas function components use the `useState()` hook.  
> Third, simplicity: function components avoid the ambiguity of the JavaScript `this` keyword and involve significantly less boilerplate code."

---

## Category 5: Props vs. State

### Q19: What is the difference between Props and State?
> **Answer:**  
> "The key difference is ownership and mutability:
> - **Props (Properties)** are passed down from a parent component to a child component (like function arguments). Props are **read-only** and immutable to the child receiving them.
> - **State** is internal data managed and owned by the component itself (like local variables). State is **mutable** via its setter function (`setCount`), and whenever state changes, the component re-renders to reflect the new data."

### Q20: How did you implement props in Practical 4 (`StudentProps.jsx`)?
> **Answer:**  
> "In `StudentProps.jsx`, the parent component `StudentProps` defines an array of student objects (`studentsList`). It iterates over this array using `.map()` and renders a child component `<StudentCard />` for each student, passing `name={student.name}` and `branch={student.branch}` as props. The child component receives these props via `function StudentCard({ name, branch })` and displays them."

### Q21: Why do we provide a `key` prop when rendering lists with `.map()` in React?
> **Answer:**  
> "React uses the `key` prop to identify each element in a dynamic list during its reconciliation process. If an item is added, removed, or reordered, the unique key allows React to update only the modified item rather than re-rendering the entire list."

---

## Category 6: React Hooks

### Q22: What are React Hooks, and what are the rules of hooks?
> **Answer:**  
> "Hooks are special functions introduced in React 16.8 that allow function components to 'hook into' React features like state and lifecycle methods without writing a class.  
> Two fundamental rules must be followed:
> 1. Only call hooks at the **top level** of your component (never inside loops, conditions, or nested functions).
> 2. Only call hooks from **React function components** or custom hooks (never from standard JavaScript functions or class components)."

### Q23: How does `useState` work in Practical 2 (`StateCounter.jsx`)?
> **Answer:**  
> "`useState(0)` initializes a state variable with the value `0`. It returns an array of two items: the current state value (`count`), and a updater function (`setCount`). When the user clicks the '+' button, our event handler calls `setCount(prev => prev + 1)`. React schedules a re-render of `StateCounter`, and on the next render, `count` holds the updated number, instantly refreshing the screen."

### Q24: What is `useRef`, and how did you use it in Practical 5 (`HooksDemo.jsx`)?
> **Answer:**  
> "`useRef` creates a mutable reference object with a `.current` property that persists across renders without causing a re-render when changed. In Practical 5, we declared `const inputRef = useRef(null)` and attached it to our `<input ref={inputRef} />`. When the user clicks the 'Focus Input' button, we execute `inputRef.current.focus()`, directly focusing the input field using native DOM methods."

### Q25: What is `useEffect`, and how did you demonstrate it in Practical 5?
> **Answer:**  
> "`useEffect` lets us synchronize a component with external systems or perform side effects (such as updating the document title, fetching data, or timers) after rendering. In `HooksDemo.jsx`, we wrote:  
> `useEffect(() => { document.title = \`Count: \${hookCount} | WAF Lab\`; }, [hookCount]);`  
> Every time `hookCount` changes, React executes this effect and synchronizes the browser tab title. Because we included `[hookCount]` in the dependency array, it only runs when `hookCount` actually changes."

### Q26: What is the dependency array in `useEffect`, and what happens if you omit it?
> **Answer:**  
> "The dependency array is the second argument to `useEffect`:
> - If you provide `[dependency]`, the effect runs only when that variable changes.
> - If you provide an empty array `[]`, the effect runs only **once** when the component mounts.
> - If you omit the dependency array completely, the effect runs **after every single render**, which can cause performance issues or infinite loops if the effect modifies state."

---

## Category 7: Project Setup, Ports, and Debugging

### Q27: Why do Express and Vite run on different ports?
> **Answer:**  
> "In computer networking, only one process can listen to a specific TCP port at a time. In our architecture:
> - Port `3000` is dedicated to our backend Express server (`server.js`), handling static file serving and `/api/student`.
> - Port `5173` is dedicated to Vite's local development server, which bundles and hot-reloads our React components.  
> They run in separate terminal windows as independent processes."

### Q28: What is Vite, and why is it preferred over `create-react-app`?
> **Answer:**  
> "Vite is a modern frontend build tool developed by Evan You. Unlike older tools like `create-react-app` (which use Webpack and re-bundle the whole project on every change), Vite leverages native ES modules in the browser during development. This provides near-instant server start (under 300ms) and lightning-fast Hot Module Replacement (HMR)."

### Q29: What would happen if you tried to run `npm start` in `express-fetch` while port 3000 was already in use?
> **Answer:**  
> "Node.js would throw an `EADDRINUSE: address already in use :::3000` exception, and the server process would crash. To resolve this, we would either terminate the process currently occupying port 3000 (using `netstat -ano` and `taskkill` on Windows) or change `const PORT = 3001` in `server.js`."

### Q30: What is CORS, and why didn't we encounter CORS errors in Practical 1?
> **Answer:**  
> "CORS stands for Cross-Origin Resource Sharing. It is a browser security mechanism that restricts web pages from making HTTP requests to a different domain, protocol, or port than the one that served the page.  
> In Practical 1, we did not get a CORS error because Express served `index.html` from `http://localhost:3000`, and the client-side JavaScript sent its fetch request to `/api/student` on the exact same origin (`http://localhost:3000`). Because the origin matches, it is a same-origin request and CORS restrictions do not apply."

---

## Quick Reference Summary for Examiners

| Practical | Concept | Key File | Primary API / Syntax |
|:---|:---|:---|:---|
| **Practical 1** | Express Server + Fetch | `server.js`, `public/index.html` | `app.use(express.static())`, `app.get('/api/student')`, `fetch()`, `async/await` |
| **Practical 2** | React State | `StateCounter.jsx` | `const [count, setCount] = useState(0)` |
| **Practical 3** | React Class Component | `ClassStudent.jsx` | `class ClassStudent extends Component`, `render()` |
| **Practical 4** | React Props | `StudentProps.jsx` | `<StudentCard name={...} branch={...} />`, `.map()` |
| **Practical 5** | Three React Hooks | `HooksDemo.jsx` | `useState` (state), `useRef` (DOM focus), `useEffect` (tab title) |
| **Practical 6** | React Function Component | `FunctionStudent.jsx` | `function FunctionStudent() { return (...) }` |
