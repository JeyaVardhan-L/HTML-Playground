# Web Application Framework — Assignment

**Module:** Web Application Framework  
**Contents:** RESTful API · React Hooks/Props/State · Express Middleware · next() Chain · React Context

---

## Repository Layout

```
Assignment/
├── backend/                  ← Requirement 1 — RESTful Book API
│   ├── app.js
│   ├── routes/books.js
│   ├── controllers/bookController.js
│   ├── models/bookModel.js
│   └── package.json
│
├── frontend/                 ← Requirements 2 & 5 — React
│   └── src/
│       ├── App.jsx           ← Props + State + Hooks demo
│       ├── App.css
│       ├── main.jsx
│       ├── components/
│       │   ├── StudentCard.jsx   ← Props demo (child)
│       │   ├── Department.jsx    ← Middle component (context passthrough)
│       │   └── StudentInfo.jsx   ← Context consumer
│       └── context/
│           └── StudentContext.js ← Context creation
│
├── middleware-demo/          ← Requirements 3 & 4 — Middleware
│   ├── app.js
│   └── package.json
│
└── README.md                 ← This file (study before viva)
```

---

## How to Run

### Backend (Book API)
```bash
cd Assignment/backend
npm install        # first time only
npm start
# Server: http://localhost:4000
```

### Middleware Demo
```bash
cd Assignment/middleware-demo
npm install        # first time only
npm start
# Server: http://localhost:4001
```

### Frontend (React)
```bash
cd Assignment/frontend
npm install        # first time only
npm run dev
# Opens: http://localhost:5173
```

---

---

# REQUIREMENT 1 — RESTful Book API

## Objective

Build a RESTful HTTP API using Express that allows a client to retrieve books, update an author, and delete expensive books. All data is stored in memory — no database required.

---

## File: `backend/models/bookModel.js`

### Block 1 — The in-memory data store

```js
let books = [
  { id: 1, title: "Clean Code", author: "Robert C. Martin", price: 150 },
  { id: 2, title: "The Pragmatic Programmer", author: "Andy Hunt", price: 175 },
  // ... more books
];
```

`books` is a plain JavaScript array that lives in memory while the server is running. Each object represents one book with four fields. Because this variable is declared with `let`, it can be reassigned — which is needed when books are deleted.

### Block 2 — Functions that operate on the data

```js
function getAllBooks() {
  return books;
}

function findBookById(id) {
  return books.find((b) => b.id === id);
}

function updateBookAuthor(id, newAuthor) {
  const book = findBookById(id);
  if (!book) return null;
  book.author = newAuthor;
  return book;
}

function deleteExpensiveBooks() {
  const removed = books.filter((b) => b.price > 190);
  books = books.filter((b) => b.price <= 190);
  return removed;
}
```

Each function has a single responsibility. `findBookById` uses `Array.find()` to locate one item. `updateBookAuthor` mutates the found object directly. `deleteExpensiveBooks` first captures the books that will be removed (so they can be returned in the response), then reassigns `books` to contain only the remaining ones.

### Block 3 — Exporting the functions

```js
module.exports = { getAllBooks, findBookById, updateBookAuthor, deleteExpensiveBooks };
```

Node.js uses CommonJS modules. `module.exports` makes these four functions available to any file that `require()`s this module.

---

## File: `backend/controllers/bookController.js`

### Block 1 — getAllBooks

```js
function getAllBooks(req, res) {
  const books = bookModel.getAllBooks();
  res.status(200).json({ success: true, count: books.length, data: books });
}
```

`req` carries the incoming request. `res` is used to send the response. `res.status(200)` sets HTTP status 200 (OK). `.json()` serialises the object to JSON and sends it.

### Block 2 — updateAuthor (validation + response)

```js
function updateAuthor(req, res) {
  const id = parseInt(req.params.id, 10);
  const { author } = req.body;

  if (!author || typeof author !== "string" || author.trim() === "") {
    return res.status(400).json({ success: false, message: "Author field is required..." });
  }

  const updated = bookModel.updateBookAuthor(id, author.trim());

  if (!updated) {
    return res.status(404).json({ success: false, message: `Book with id ${id} not found.` });
  }

  res.status(200).json({ success: true, data: updated });
}
```

`req.params.id` extracts the `:id` segment. `parseInt()` converts it from string to number. `req.body.author` contains the JSON field. Three outcomes: bad input → 400, not found → 404, success → 200.

### Block 3 — deleteExpensive

```js
function deleteExpensive(req, res) {
  const removed = bookModel.deleteExpensiveBooks();
  res.status(200).json({
    success: true,
    message: `${removed.length} book(s) with price > 190 deleted.`,
    deletedCount: removed.length,
    deletedBooks: removed,
  });
}
```

The model filters; the controller formats the JSON response showing exactly what was deleted.

---

## File: `backend/routes/books.js`

```js
const router = express.Router();

router.get("/", bookController.getAllBooks);
router.put("/:id/author", bookController.updateAuthor);
router.delete("/expensive", bookController.deleteExpensive);
```

`express.Router()` groups related routes. The router mounts at `/api/books` in `app.js`. `/expensive` is defined before `/:id` so Express does not treat the string "expensive" as an id.

---

## File: `backend/app.js`

```js
app.use(express.json());
```

Built-in middleware that parses JSON request bodies. Without this, `req.body` would be undefined.

```js
app.use((req, res, next) => {
  console.log(`[${new Date().toISOString()}] ${req.method} ${req.url}`);
  next();
});
```

Request logger — every request passes through, is logged, then control is passed forward with `next()`.

```js
app.use("/api/books", booksRouter);
```

Mounts the books router at `/api/books`.

```js
app.use((err, req, res, next) => {
  res.status(500).json({ success: false, message: "Internal server error." });
});
```

Four-parameter signature identifies this as error-handling middleware. Express calls it when `next(err)` is used.

---

## API Demonstration

### GET /api/books

```
GET http://localhost:4000/api/books
```

Response:
```json
{
  "success": true,
  "count": 8,
  "data": [
    { "id": 1, "title": "Clean Code", "author": "Robert C. Martin", "price": 150 }
  ]
}
```

### PUT /api/books/1/author

```
PUT http://localhost:4000/api/books/1/author
Content-Type: application/json

{ "author": "Uncle Bob" }
```

Response:
```json
{
  "success": true,
  "message": "Author updated successfully.",
  "data": { "id": 1, "title": "Clean Code", "author": "Uncle Bob", "price": 150 }
}
```

### DELETE /api/books/expensive

```
DELETE http://localhost:4000/api/books/expensive
```

Response:
```json
{
  "success": true,
  "message": "3 book(s) with price > 190 deleted.",
  "deletedCount": 3,
  "deletedBooks": [
    { "id": 4, "title": "You Don't Know JS", "price": 200 },
    { "id": 5, "title": "Design Patterns", "price": 210 },
    { "id": 6, "title": "Introduction to Algorithms", "price": 195 }
  ]
}
```

---

---

# REQUIREMENT 2 — REACT HOOKS, PROPS AND STATE

## Objective

Demonstrate Props, State, and Hooks in a Student Dashboard application.

---

## Props Demo — `frontend/src/components/StudentCard.jsx`

```jsx
function StudentCard({ student }) {
  return (
    <div className="card">
      <h3>{student.name}</h3>
      <p>Roll No: {student.rollNo}</p>
    </div>
  );
}
```

Props are how a parent sends data to a child. `App` renders `<StudentCard student={s} />`. Inside `StudentCard`, `{ student }` destructures the props. The component can read the prop but cannot modify it. Props are read-only.

**Execution flow:** App renders → React calls StudentCard with the student object → StudentCard returns JSX → React converts to HTML.

---

## State Demo — `frontend/src/App.jsx`

```jsx
const [selectedIndex, setSelectedIndex] = useState(0);
const [attendanceCount, setAttendanceCount] = useState(0);
```

`useState` returns `[currentValue, setterFunction]`. When `setSelectedIndex` is called with a new value, React re-renders the component and all children see the updated value.

```jsx
<select onChange={(e) => setSelectedIndex(Number(e.target.value))}>
```

User picks a student → `onChange` fires → calls `setSelectedIndex` → React re-renders → new student shown.

```jsx
<button onClick={() => setAttendanceCount((c) => c + 1)}>
  Mark Attendance
</button>
```

Each click increments the counter. The display updates immediately because React re-renders on state change.

---

## useEffect Demo — `frontend/src/App.jsx`

```jsx
const [title, setTitle] = useState("Student Dashboard");

useEffect(() => {
  document.title = title;
}, [title]);
```

`useEffect` runs after every render where `title` has changed. `document.title` is a side effect — it is outside React's control. The dependency array `[title]` tells React to only re-run this effect when `title` changes. Type in the title input field and watch the browser tab title update.

---

---

# REQUIREMENT 3 — EXPRESS MIDDLEWARE

## What is Middleware?

Middleware is a function that runs between an incoming HTTP request and the final route handler. It can inspect, modify, or even stop the request.

Every middleware function receives three arguments:

- `req` — the request object. Contains the URL, method, headers, body, and any data attached by earlier middleware.
- `res` — the response object. Used to send a response back to the client.
- `next` — a callback function. Calling `next()` passes control to the next middleware. Not calling it stops the request chain.

## Request Flow

```
Client HTTP Request
       ↓
express.json()           ← Built-in middleware (parses JSON body)
       ↓
Logger middleware         ← Application-level middleware
       ↓
/api/books router         ← Router-level middleware
       ↓
Route handler             ← Controller function
       ↓
Client HTTP Response
```

## Types of Middleware

### 1. Application-Level Middleware

```js
app.use((req, res, next) => {
  console.log(`${req.method} ${req.url}`);
  next();
});
```

Registered with `app.use()`. Runs for every request regardless of URL or method.

### 2. Router-Level Middleware

```js
const router = express.Router();
router.use((req, res, next) => {
  console.log("Books router request");
  next();
});
```

Registered on a Router instance. Only runs for requests that reach that router.

### 3. Error-Handling Middleware

```js
app.use((err, req, res, next) => {
  res.status(500).json({ error: err.message });
});
```

Has four parameters — Express identifies it by count. Called when `next(err)` is used.

### 4. Built-In Middleware

```js
app.use(express.json());
app.use(express.static("public"));
```

Included in Express — no additional installation needed.

### 5. Third-Party Middleware

```js
const morgan = require("morgan");
app.use(morgan("dev"));
```

Installed via npm. Added only when built-in options are insufficient.

---

---

# REQUIREMENT 4 — next() MULTI-LAYER EXAMPLE

## File: `middleware-demo/app.js`

## Objective

Show middleware execution order and demonstrate what stops when `next()` is not called.

## The Chain

```js
app.use(middlewareOne);   // logs request
app.use(middlewareTwo);   // validates method
app.use(middlewareThree); // attaches timestamp

app.get("/", (req, res) => {
  res.json({ message: "Hello from route!", requestReceivedAt: req.requestTime });
});
```

For `GET /`, the console prints:
```
Middleware 1: Request received. Logging the incoming request.
Middleware 2: Checking if request method is allowed.
Middleware 3: Adding a timestamp to the request object.
Route handler: Sending the response.
```

Each middleware calls `next()`, passing control forward.

## When next() Is NOT Called

```js
app.get("/stop-early", middlewareOne, (req, res, next) => {
  console.log("STOP-EARLY: Does NOT call next().");
  res.json({ message: "Stopped here." });
}, (req, res) => {
  console.log("This will never run.");
});
```

The second function sends a response but never calls `next()`. The third function (the intended handler) never executes. This is how middleware can short-circuit the request.

Console output for `GET /stop-early`:
```
Middleware 1: Request received. Logging the incoming request.
STOP-EARLY: Does NOT call next().
```

---

---

# REQUIREMENT 5 — REACT CONTEXT

## Objective

Demonstrate how Context passes data through a component tree without prop drilling.

## The Problem Without Context

```
App (has student data)
  → Department (must receive and forward student — even though it doesn't use it)
    → StudentInfo (finally uses the data)
```

This is prop drilling — intermediate components carry data they do not need.

## Step 1 — Create the Context

```js
import { createContext } from "react";
const StudentContext = createContext(null);
export default StudentContext;
```

`createContext(null)` creates the context channel. `null` is the default value when no Provider is present.

## Step 2 — Provide the Value

```jsx
<StudentContext.Provider value={selectedStudent}>
  <Department name={selectedStudent.department} />
</StudentContext.Provider>
```

The Provider wraps the component tree. `value={selectedStudent}` is what every consumer will receive. When `selectedStudent` changes, all consumers re-render automatically.

## Step 3 — Middle Component Does NOT Forward

```jsx
function Department({ name }) {
  return (
    <div>
      <h3>Department: {name}</h3>
      <StudentInfo />
    </div>
  );
}
```

`Department` only knows about `name`. It does not know or care about the student data. Yet it renders `StudentInfo` which needs it.

## Step 4 — Consume the Context

```jsx
function StudentInfo() {
  const student = useContext(StudentContext);
  return <p>{student.name} — {student.rollNo}</p>;
}
```

`useContext(StudentContext)` reads the current value from the nearest Provider above it. No prop was passed — the data arrives through context.

**Hierarchy:**
```
App (Provider — supplies selectedStudent)
  └── Department (middle layer — unaware of student context)
        └── StudentInfo (consumer — reads student from context)
```

---

---

# VIVA PREPARATION — 15 Most Likely Questions

| # | Question | Answer |
|---|----------|--------|
| 1 | What is a RESTful API? | Uses HTTP methods (GET/POST/PUT/DELETE) on resources identified by URLs. Stateless — each request is self-contained. |
| 2 | What HTTP status codes did you use? | 200 OK, 400 Bad Request, 404 Not Found, 500 Internal Server Error. |
| 3 | Why use express.Router()? | Groups related routes together. Keeps app.js clean. Allows mounting at any prefix. |
| 4 | What is middleware? | A function with (req, res, next) that runs between the request arriving and the route handler executing. |
| 5 | What does next() do? | Passes control to the next middleware or route. Without it the request hangs. |
| 6 | Difference between app.use() and app.get()? | app.use() matches all HTTP methods. app.get() only matches GET requests. |
| 7 | What are Props? | Read-only data passed from parent to child component. The child renders what it receives. |
| 8 | What is State? | Data managed inside a component that can change. useState creates state; calling the setter triggers a re-render. |
| 9 | Why useState instead of a plain variable? | Plain variable changes do not trigger re-renders. useState notifies React that a re-render is needed. |
| 10 | What is useEffect? | Runs code after rendering. Used for side effects like DOM manipulation, timers, or data fetching. |
| 11 | What is React Context? | A way to share data across a component tree without passing props through every intermediate level. |
| 12 | What does createContext() do? | Creates a Context object — the channel for data. The argument is the default value when no Provider exists. |
| 13 | What is prop drilling? | Passing data through many intermediate components just to reach a deeply nested one. Context avoids this. |
| 14 | Application-level vs router-level middleware? | App-level runs for all requests. Router-level only runs for requests that reach that specific router. |
| 15 | How does Express identify error-handling middleware? | By the four-parameter signature (err, req, res, next). Regular middleware has three. |
