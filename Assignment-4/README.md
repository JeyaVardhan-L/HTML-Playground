# Web Application Frameworks (WAF) — Lab Assignment 4
## Express Fetch + React Practicals & Beginner Learning Guide

**Subject:** Web Application Frameworks (WAF) Lab  
**Assignment:** Lab Assignment 4 — Express Server with Browser Fetch & Core React Practicals  
**Technologies:** Node.js, Express.js, React 18, Vite (Vanilla JS & JSX, Zero External Frameworks/APIs)  
**Student:** Jey (Roll No: 9057) · Department of Computer Science & Engineering, GITAM University  

---

## 1. Assignment Overview

**Assignment 4** covers modern full-stack web development techniques split into two cohesive, lightweight projects:
1. **Server-Side & Asynchronous Fetch (`express-fetch/`)**: A dedicated Node.js + Express backend server serving static HTML and providing an asynchronous `GET /api/student` JSON endpoint.
2. **Component-Based UI Architecture (`react-practicals/`)**: A clean React project powered by Vite implementing five dedicated components that demonstrate the core mechanisms of React (State, Class Components, Props, Three Hooks, and Function Components).

---

## 2. Directory Structure

```text
Assignment-4/
├── README.md                      ← Overview, setup instructions, testing checklist & topic mapping
├── express-fetch/                 ← Practical 1: Backend Express Server + Browser Fetch
│   ├── package.json               ← Express dependency & start script
│   ├── server.js                  ← Express server, static middleware, and GET /api/student endpoint
│   └── public/
│       └── index.html             ← Frontend HTML client using async/await fetch()
├── react-practicals/              ← Practicals 2–6: React Laboratory (Vite + React)
│   ├── package.json               ← React 18, React-DOM, Vite & plugin-react
│   ├── vite.config.js             ← Vite build configuration
│   ├── index.html                 ← HTML host page for the React root mount
│   └── src/
│       ├── main.jsx               ← React DOM root entry point
│       ├── App.jsx                ← Main tabbed container housing all 5 React practicals
│       ├── styles.css             ← Neutral, college-practical CSS styling
│       └── components/
│           ├── StateCounter.jsx   ← Practical 2: React State (useState) increment & decrement
│           ├── ClassStudent.jsx   ← Practical 3: React Class Component (extends Component, render())
│           ├── StudentProps.jsx   ← Practical 4: React Props (Parent to child data passing via .map())
│           ├── HooksDemo.jsx      ← Practical 5: Three React Hooks (useState, useRef, useEffect)
│           └── FunctionStudent.jsx← Practical 6: React Function Component (Modern JSX return)
└── docs/
    └── learning/
        ├── START-HERE.md          ← Orientation, mental models, and reading roadmap
        ├── REACT-FROM-ZERO.md     ← Foundational React theory (JSX, components, state, props, hooks)
        ├── EXPRESS-AND-FETCH.md   ← Express server architecture, HTTP requests, JSON & async/await fetch
        ├── CODE-EXPLANATION.md    ← Line-by-line explanation of all 6 practicals and interaction traces
        ├── VIVA-PREP.md           ← 26 high-yield viva questions with concise spoken model answers
        ├── HANDS-ON-EXERCISES.md  ← 10 beginner coding exercises with hints and expected outcomes
        └── GLOSSARY.md            ← Full-stack glossary of terms
```

---

## 3. The Six Practicals at a Glance

| Practical | Project / Component | Topic / Requirement | Key Feature |
| :--- | :--- | :--- | :--- |
| **Practical 1** | `express-fetch/` | Express Server & Browser Fetch | Separate HTTP requests: initial page load vs. asynchronous `fetch('/api/student')` with terminal server logging. |
| **Practical 2** | `StateCounter.jsx` | React State: Increment & Decrement | Interactive counter using `useState(0)`, updating the UI immediately on state change. |
| **Practical 3** | `ClassStudent.jsx` | React Class Component | ES6 class extending `React.Component`, constructor state, and required `render()` method. |
| **Practical 4** | `StudentProps.jsx` | React Props | Parent component passing data array down to reusable `<StudentCard />` child components. |
| **Practical 5** | `HooksDemo.jsx` | Three React Hooks | Combines `useState` (counter & text), `useRef` (DOM node focus), and `useEffect` (tab title sync). |
| **Practical 6** | `FunctionStudent.jsx` | React Function Component | Modern standard JavaScript function returning JSX to describe the student record UI. |

---

## 4. Prerequisites & Installation

Make sure Node.js (v18 or higher) and npm are installed on your system:
```powershell
node -v
npm -v
```

### Installing Dependencies

Both projects have their own lightweight `package.json`. Run `npm install` inside each folder:

```powershell
# 1. Install Express for Practical 1:
cd c:\Users\user\Downloads\HTML-Playground\HTML-Playground\Assignment-4\express-fetch
npm install

# 2. Install React and Vite for Practicals 2-6:
cd c:\Users\user\Downloads\HTML-Playground\HTML-Playground\Assignment-4\react-practicals
npm install
```

---

## 5. How to Run the Projects

> [!IMPORTANT]
> The **Express Server (Practical 1)** and the **Vite React Server (Practicals 2–6)** run on **different ports** and should be started in **separate terminal windows**.

### Terminal 1: Running Practical 1 (Express Server)
```powershell
cd c:\Users\user\Downloads\HTML-Playground\HTML-Playground\Assignment-4\express-fetch
npm start
```
- **Local URL**: `http://localhost:3000`
- **API URL**: `http://localhost:3000/api/student`
- **Output**: Serves `public/index.html`. Watch this terminal log whenever you click "Fetch Data" in the browser!

### Terminal 2: Running Practicals 2–6 (React + Vite)
```powershell
cd c:\Users\user\Downloads\HTML-Playground\HTML-Playground\Assignment-4\react-practicals
npm run dev
```
- **Local URL**: `http://localhost:5173`
- **Output**: Opens the React Core Concepts Laboratory with interactive tabs for Practicals 2 through 6.

---

## 6. Demonstration & Testing Checklist

### Testing Practical 1 (Express & Fetch):
- [ ] Open `http://localhost:3000` in your browser. Verify the page displays "Student Information" but **no student data is shown initially**.
- [ ] Click the **"Fetch Data"** button.
- [ ] Verify the loading indicator flashes and the green student record box appears with Name: `Jey`, Roll No: `9057`, Branch: `Computer Science & Engineering`.
- [ ] Check Terminal 1: Confirm the server printed: `[EXPRESS SERVER ...] Received GET request for /api/student`.
- [ ] Click **"Clear Display"**: Confirm the student card clears.

### Testing Practical 2 (React State):
- [ ] In the React app (`http://localhost:5173`), click **"Practical 2: State Counter"**.
- [ ] Initial count is `0`.
- [ ] Click **"+ Increment"** twice → Count updates to `2`.
- [ ] Click **"− Decrement"** once → Count updates to `1`.
- [ ] Click **"Reset"** → Count returns to `0`.

### Testing Practical 3 (React Class Component):
- [ ] Click **"Practical 3: Class Component"**.
- [ ] Verify the student profile renders displaying student name, branch, semester, and bio from `this.state`.
- [ ] Verify the explanation card clearly contrasts class components with function components.

### Testing Practical 4 (React Props):
- [ ] Click **"Practical 4: Props"**.
- [ ] Verify that 3 distinct student cards render (Jey, Aarav Sharma, Priya Nair).
- [ ] Verify each card displays its specific branch, roll number, and year passed down as props from the parent array.

### Testing Practical 5 (Three Hooks):
- [ ] Click **"Practical 5: Three Hooks"**.
- [ ] **Hook 1 & 3 (`useState` + `useEffect`)**: Click "+ Increase Counter". Verify the count increments AND the browser tab title updates to: `Clicked 1 times — Hooks Demo`.
- [ ] **Hook 1 & 2 (`useState` + `useRef`)**: Type into the text field (verifying `useState` live preview). Then click **"🔍 Focus Input Box"** and verify the cursor jumps directly into the text field using the `useRef` node reference.

### Testing Practical 6 (React Function Component):
- [ ] Click **"Practical 6: Function Component"**.
- [ ] Verify the student record renders cleanly using modern JSX returned from a pure function.

---

## 7. Topic-to-Practical Mapping Matrix

| Lab Topic | File / Component | Code Evidence |
| :--- | :--- | :--- |
| **Express Server** | `express-fetch/server.js` | `const app = express(); app.listen(3000)` |
| **Static File Serving** | `express-fetch/server.js` | `app.use(express.static(path.join(__dirname, "public")))` |
| **JSON API Endpoint** | `express-fetch/server.js` | `app.get("/api/student", (req, res) => res.json(studentData))` |
| **Browser Fetch API** | `express-fetch/public/index.html` | `const response = await fetch("/api/student"); const data = await response.json();` |
| **Async / Await & Error Handling** | `express-fetch/public/index.html` | `async function fetchStudentData() { try { ... } catch (error) { ... } }` |
| **React State (`useState`)** | `StateCounter.jsx` | `const [count, setCount] = useState(0); setCount(count + 1);` |
| **React Class Component** | `ClassStudent.jsx` | `class ClassStudent extends Component { render() { return ... } }` |
| **React Props** | `StudentProps.jsx` | `<StudentCard name={student.name} branch={student.branch} />` |
| **List Rendering (`.map()`)** | `StudentProps.jsx` | `{studentsList.map((student) => <StudentCard key={student.id} ... />)}` |
| **React Ref (`useRef`)** | `HooksDemo.jsx` | `const inputRef = useRef(null); inputRef.current.focus();` |
| **React Effect (`useEffect`)** | `HooksDemo.jsx` | `useEffect(() => { document.title = ...; return () => { ... } }, [clicks]);` |
| **React Function Component** | `FunctionStudent.jsx` | `function FunctionStudent() { return (<div>...</div>); }` |

---

## 8. Learning Documentation

Start your review with the comprehensive guides in [`docs/learning/`](docs/learning/):

1. [**`START-HERE.md`**](docs/learning/START-HERE.md) — Big picture orientation, architecture diagrams, and learning sequence.
2. [**`REACT-FROM-ZERO.md`**](docs/learning/REACT-FROM-ZERO.md) — Plain-English explanation of JSX, components, props, state, and hooks.
3. [**`EXPRESS-AND-FETCH.md`**](docs/learning/EXPRESS-AND-FETCH.md) — Deep dive into Express backend, HTTP methods, JSON, and client fetch.
4. [**`CODE-EXPLANATION.md`**](docs/learning/CODE-EXPLANATION.md) — Line-by-line walkthrough of all 6 practicals and interaction traces.
5. [**`VIVA-PREP.md`**](docs/learning/VIVA-PREP.md) — 26 high-yield viva questions with concise spoken model answers.
6. [**`HANDS-ON-EXERCISES.md`**](docs/learning/HANDS-ON-EXERCISES.md) — 10 guided coding exercises with hints and expected outcomes.
7. [**`GLOSSARY.md`**](docs/learning/GLOSSARY.md) — Full-stack terminology cheat sheet.
