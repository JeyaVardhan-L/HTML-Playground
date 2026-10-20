# Express and Fetch: Server-Side and Client-Side Communication

This guide explains the backend and network communication principles implemented in **Practical 1** (`Assignment-4/express-fetch/`). Every concept, route, function, and filename discussed here matches our real code.

---

## 1. What is a Server? What is Node.js?

Before Express, JavaScript could only run inside a web browser (like Chrome or Firefox).

In 2009, Ryan Dahl created **Node.js**. Node.js is an open-source runtime environment built on Chrome's V8 engine that allows developers to run JavaScript **directly on an operating system** (Windows, macOS, Linux).

With Node.js, JavaScript can:
- Read and write files to the hard drive.
- Open network sockets and listen on a **port** (like `3000`).
- Act as an HTTP **Web Server**.

---

## 2. What Does Express.js Do?

**Express.js** is the most popular, minimalist web server framework for Node.js. 

Writing a raw HTTP server in vanilla Node.js requires handling complex streams and headers manually. Express makes this trivial by providing three core features:
1. **Routing**: Defining what happens when a client sends a request to a specific URL (e.g. `app.get("/api/student", ...)`).
2. **Middleware**: Modular functions that run during the request cycle (e.g. `app.use(express.static(...))` to serve images, CSS, and HTML files).
3. **HTTP Response Helpers**: Simple methods like `res.sendFile(...)` and `res.json(...)` that automatically set correct HTTP headers and status codes.

---

## 3. The Architecture of `server.js`

Here is the complete implementation of our server in `Assignment-4/express-fetch/server.js`:

```javascript
const express = require("express");
const path = require("path");

const app = express();
const PORT = process.env.PORT || 3000;

// 1. Static Middleware: Serves all files from the "public" folder
app.use(express.static(path.join(__dirname, "public")));

// 2. Hardcoded Student Data
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

// 3. API Route: GET /api/student
app.get("/api/student", (req, res) => {
  const timestamp = new Date().toLocaleTimeString();
  console.log(`[EXPRESS SERVER ${timestamp}] Received GET request for /api/student`);
  res.json(studentData);
});

// 4. Fallback Default Route
app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "index.html"));
});

// 5. Start listening for incoming connections
app.listen(PORT, () => {
  console.log(`🚀 Express Server is running on http://localhost:${PORT}`);
});
```

### Breaking Down the Code:
- `express()`: Initializes an Express application instance (`app`).
- `PORT = 3000`: The door number on our computer through which network traffic enters.
- `app.use(express.static(...))`: Whenever a browser asks for `/index.html` or CSS, Express automatically serves it from `public/`.
- `app.listen(PORT, ...)`: Binds the application to port 3000 and starts waiting for incoming requests.

---

## 4. Serving the HTML vs. Fetching the Data: Two Separate Requests

A common beginner mistake is assuming that web applications load everything in one go. In modern web architecture, pages work in stages:

```text
Request 1: Initial Page Load
Browser: "GET http://localhost:3000/"  --> Express sends public/index.html
(Page displays "Student Information" heading and "Fetch Data" button. NO student data is visible!)

--- Time passes (User looks at the screen) ---

Request 2: Dynamic Data Request
User clicks "Fetch Data" button!
Browser executes: fetch("/api/student") --> Express sends JSON object { name: "Jey", ... }
Browser DOM updates to show the green student card!
```

### Why Do We Separate These?
1. **Speed**: The initial HTML shell loads instantly.
2. **Reusability**: The same API endpoint (`/api/student`) can be consumed by a web browser, a mobile app, or an automated testing tool.
3. **No Blinking**: The webpage does not reload or flicker when new data arrives.

---

## 5. What Does `GET /api/student` Mean?

Every web interaction is built on the **HTTP (Hypertext Transfer Protocol)**:
- **HTTP Method (`GET`)**: The verb describing what the client wants to do. `GET` means "please retrieve information without modifying anything on the server."
- **Path (`/api/student`)**: The specific route on the server handling this request.
- **Prefix (`/api/`)**: A universal web development convention that indicates this route returns raw computer data (JSON), rather than an HTML webpage.

---

## 6. What is JSON?

**JSON** stands for **JavaScript Object Notation**. It is a standardized, text-based data exchange format that looks almost identical to a JavaScript object literal:

```json
{
  "name": "Jey",
  "rollNo": "9057",
  "branch": "Computer Science & Engineering"
}
```

- In `server.js`, `res.json(studentData)` converts our JavaScript object into a JSON text string and sets the HTTP header `Content-Type: application/json`.
- In the browser, `await response.json()` parses the incoming JSON text back into a live JavaScript object that we can access using `data.name` or `data.rollNo`.

---

## 7. How the Browser Client Works: `fetch()`, `async/await`, and `try/catch`

Inside `Assignment-4/express-fetch/public/index.html`:

```javascript
async function fetchStudentData() {
  // Step 1: UI feedback
  loadingIndicator.style.display = "block";
  fetchBtn.disabled = true;

  try {
    // Step 2: Send HTTP GET request asynchronously
    const response = await fetch("/api/student");

    // Step 3: Check if the server answered with an error status (like 404 or 500)
    if (!response.ok) {
      throw new Error(`Server returned HTTP ${response.status}: ${response.statusText}`);
    }

    // Step 4: Parse the JSON body
    const data = await response.json();

    // Step 5: Update the DOM with the received student data
    studentName.textContent = data.name;
    studentRoll.textContent = data.rollNo;
    studentBranch.textContent = data.branch;
    studentContainer.style.display = "block";

  } catch (error) {
    // Step 6: Handle network or server failure gracefully
    errorBox.textContent = `⚠ Failed to fetch: ${error.message}`;
    errorBox.style.display = "block";

  } finally {
    // Step 7: Cleanup UI
    loadingIndicator.style.display = "none";
    fetchBtn.disabled = false;
  }
}
```

### Explaining the Important Syntax:
- `async`: Declares that this function handles asynchronous (non-blocking) tasks.
- `await`: Pauses execution of *this function* until the network promise resolves, without freezing the browser UI or other scripts.
- `response.ok`: A boolean property that is `true` if the HTTP status code is between 200 and 299.
- `try/catch`: Protects your application from crashing if the server is offline or the network drops.
- `finally`: Guarantees that the loading indicator is hidden and the button is re-enabled, whether the request succeeded or failed.

---

## 8. Reading Terminal Logs & Browser DevTools

When running Practical 1:

1. **In Terminal 1 (Node.js Server Output)**:
   ```text
   ==================================================
   🚀 Express Server is running!
   🌐 Open in browser: http://localhost:3000
   📡 API endpoint:    http://localhost:3000/api/student
   ==================================================
   [EXPRESS SERVER 4:15:19 pm] Received GET request for /api/student
   ```
   Every time you click "Fetch Data", a new timestamped line prints here.

2. **In Browser Developer Tools (F12 -> Network Tab)**:
   - Filter by **Fetch/XHR**.
   - Click "Fetch Data".
   - You will see a request named `student`.
   - Click it to inspect **Headers** (`Status: 200 OK`, `Content-Type: application/json`) and **Response** (the student JSON payload).

---

## 9. Troubleshooting Common Errors

### Error A: `EADDRINUSE: address already in use :::3000`
- **Cause**: Another program (or a previously started Node process) is already running on port 3000.
- **Fix**: Either stop the other program, or run Express on a different port:
  ```powershell
  $env:PORT=3001; npm start
  ```

### Error B: `Failed to fetch: Failed to fetch / NetworkError`
- **Cause**: The Express server is not running, or you opened the HTML file directly via `file:///` instead of `http://localhost:3000`.
- **Fix**: Make sure you ran `npm start` in `express-fetch/` and visited `http://localhost:3000` in your address bar.

### Error C: `404 Not Found`
- **Cause**: The requested route does not exist (e.g. typing `/student` instead of `/api/student`).
- **Fix**: Check spelling in `server.js` and `fetch("/api/student")`.

Now let's explore React components in [REACT-FROM-ZERO.md](REACT-FROM-ZERO.md)!
