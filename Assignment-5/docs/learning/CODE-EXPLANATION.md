# Assignment 5 — Code Explanation: Line-by-Line Breakdown

This document provides a comprehensive, block-by-block explanation of the actual code in `server.js` and `public/index.html`. Every variable, route, and function discussed here matches the code in the repository.

---

## Part 1: Backend Server (`server.js`)

### 1. File Purpose
The purpose of `server.js` is to create an HTTP server using Express.js that:
1. Listens on TCP port `3001`.
2. Serves static HTML and CSS from the `public/` directory.
3. Provides an API endpoint `GET /api/student`.
4. Maintains an in-memory counter (`requestCount`) that increments with every request.
5. Generates a fresh timestamp and logs each incoming request to the terminal.

---

### 2. Code Breakdown: Logical Blocks

#### Block 1: Imports and Initialization
```javascript
const express = require("express");
const path = require("path");

const app = express();
const PORT = 3001;
```
- `require("express")`: Imports the Express library.
- `require("path")`: Imports Node's built-in module for handling file paths across different operating systems (Windows `\` vs Linux `/`).
- `const app = express()`: Initializes an Express application instance.
- `const PORT = 3001`: Sets the port number to 3001, matching the assignment specification.

#### Block 2: In-Memory State & Sample Student Data
```javascript
// 1. Server-side request counter initialized to zero
let requestCount = 0;

// 2. Sample student data stored in a simple JavaScript object
const studentData = {
  name: "Student Name",
  branch: "CSE",
  year: "3rd Year"
};
```
- `let requestCount = 0`: Defined with `let` so it can be re-assigned and incremented each time a request arrives. It lives in server memory as long as the Node process is running.
- `studentData`: An object holding student attributes: `name`, `branch`, and `year`.

#### Block 3: Static Asset Middleware
```javascript
// 3. Middleware to serve static files from the "public" directory
app.use(express.static(path.join(__dirname, "public")));
```
- `express.static()`: Built-in Express middleware that automatically serves files located in the `public` folder.
- `path.join(__dirname, "public")`: Resolves the absolute path to `Assignment-5/public`. When a browser requests `/index.html` or assets, Express serves them directly.

#### Block 4: The Dynamic API Endpoint (`GET /api/student`)
```javascript
// 4. API Endpoint: GET /api/student
app.get("/api/student", (req, res) => {
  // Increment server-side request counter
  requestCount += 1;

  // Generate a fresh timestamp on the server for this request
  const timestamp = new Date().toLocaleTimeString();

  // Log each request in the terminal in the exact required format
  console.log(`GET /api/student: request ${requestCount}`);

  // Return dynamic JSON with student fields, request number, and fresh timestamp
  res.json({
    name: studentData.name,
    branch: studentData.branch,
    year: studentData.year,
    requestNumber: requestCount,
    timestamp: timestamp
  });
});
```
- `app.get("/api/student", (req, res) => { ... })`: Registers a handler for HTTP GET requests sent to `/api/student`.
- `requestCount += 1`: Every time this route is triggered, the counter increases by 1.
- `new Date().toLocaleTimeString()`: Evaluates the exact system time when the request hit the server (e.g., `"5:32:10 PM"`).
- `console.log(...)`: Prints the required log format (`GET /api/student: request 1`) to stdout.
- `res.json({...})`: Sends an HTTP 200 OK response with the JSON payload. Notice that `requestNumber` and `timestamp` are computed dynamically on each invocation.

#### Block 5: Default Route & Server Startup
```javascript
// 5. Default route to serve public/index.html
app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "index.html"));
});

// 6. Start listening on port 3001 with explicit conflict detection
const server = app.listen(PORT, () => {
  console.log("==================================================");
  console.log(`Express server running on http://localhost:${PORT}`);
  console.log(`API endpoint: http://localhost:${PORT}/api/student`);
  console.log(`Ready to receive client requests...`);
  console.log("==================================================");
});

// Port conflict error handling
server.on("error", (err) => {
  if (err.code === "EADDRINUSE") {
    console.error(`\n[PORT CONFLICT ERROR] Port ${PORT} is already in use by another process.`);
    console.error(`Please stop the process using port ${PORT} before starting this server.\n`);
  } else {
    console.error("\n[SERVER ERROR]", err.message, "\n");
  }
});
```
- `app.get("/")`: Ensures visiting the root URL returns the `public/index.html` file.
- `app.listen(PORT, ...)`: Binds the application to port 3001 and begins listening for incoming TCP traffic.
- `server.on("error", ...)`: Checks for `EADDRINUSE` to cleanly notify the user if port 3001 is already taken by another application.

---

## Part 2: Frontend Client (`public/index.html`)

### 1. File Purpose
The purpose of `public/index.html` is to provide:
1. An explanation of how on-demand HTTP connections work.
2. A single interactive **Fetch Data** button.
3. A status area displaying loading indicators, success badges, or error messages.
4. A hidden student details table that populates dynamically upon receiving JSON.

---

### 2. Code Breakdown: Logical Blocks

#### Block 1: HTML Structure
```html
<div class="page-wrap">
  <header class="page-header">
    <span class="page-label">WAF Lab · Assignment 5</span>
    <h1>Fetch Student Data</h1>
    <p>Fetching the data with a new connection using Express js</p>
  </header>

  <main class="content">
    <div class="explanation">
      <!-- Short explanation of how it works -->
    </div>

    <div class="btn-row">
      <button id="fetchBtn" type="button">Fetch Data</button>
    </div>

    <!-- Status area -->
    <div class="status-area">
      <div id="loadingMessage">⏳ Sending new HTTP request to Express server (GET /api/student)...</div>
      <div id="statusMessage"></div>
      <div id="errorMessage"></div>
    </div>

    <!-- Initially hidden table -->
    <section id="studentDisplay" aria-live="polite">
      <h2 class="display-title">Server Response Data</h2>
      <ul class="info-list">
        <li>
          <span class="il-label">Student Name</span>
          <span class="il-value" id="studentName">—</span>
        </li>
        <!-- branch, year, requestNumber, fetchTimestamp -->
      </ul>
    </section>
  </main>
</div>
```
- `#fetchBtn`: The trigger button.
- `#loadingMessage`, `#statusMessage`, `#errorMessage`: Dynamic feedback containers.
- `#studentDisplay`: Initially has `style="display: none;"` in CSS so no student info is shown prior to clicking.

#### Block 2: DOM Element References
```javascript
const fetchBtn = document.getElementById("fetchBtn");
const loadingMessage = document.getElementById("loadingMessage");
const statusMessage = document.getElementById("statusMessage");
const errorMessage = document.getElementById("errorMessage");
const studentDisplay = document.getElementById("studentDisplay");

const studentName = document.getElementById("studentName");
const studentBranch = document.getElementById("studentBranch");
const studentYear = document.getElementById("studentYear");
const requestNumber = document.getElementById("requestNumber");
const fetchTimestamp = document.getElementById("fetchTimestamp");
```
- Caches direct references to the DOM nodes so they can be modified quickly without repeatedly querying the document tree.

#### Block 3: The `fetchStudentData()` Asynchronous Function
```javascript
async function fetchStudentData() {
  // 1. Show loading state, clear any previous errors
  loadingMessage.style.display = "block";
  statusMessage.style.display = "none";
  errorMessage.style.display = "none";
  errorMessage.textContent = "";
  fetchBtn.disabled = true;

  try {
    // 2. Send a new HTTP GET request to the Express API endpoint
    const response = await fetch("/api/student");

    // 3. Check whether the response was successful (HTTP 200-299)
    if (!response.ok) {
      throw new Error(`Server returned HTTP ${response.status} (${response.statusText})`);
    }

    // 4. Parse the JSON response body
    const data = await response.json();

    // 5. Update DOM with student data received from server
    studentName.textContent = data.name;
    studentBranch.textContent = data.branch;
    studentYear.textContent = data.year;
    requestNumber.textContent = `#${data.requestNumber}`;
    fetchTimestamp.textContent = data.timestamp;

    // 6. Display the student container and status message
    studentDisplay.style.display = "block";
    statusMessage.textContent = `✓ Request #${data.requestNumber} completed successfully at ${data.timestamp}`;
    statusMessage.style.display = "block";

  } catch (err) {
    // 7. Handle network errors or server failures gracefully
    console.error("Fetch error:", err);
    errorMessage.textContent = `Failed to fetch data: ${err.message}. Ensure the Express server is running on port 3001.`;
    errorMessage.style.display = "block";
  } finally {
    // 8. Hide loading message and re-enable button
    loadingMessage.style.display = "none";
    fetchBtn.disabled = false;
  }
}
```

- **Step 1:** Disables the button (`fetchBtn.disabled = true`) to prevent accidental double-clicks while the request is in flight. Displays the loading message.
- **Step 2:** Calls `await fetch("/api/student")`. The browser makes an asynchronous GET request.
- **Step 3:** Inspects `response.ok`. If the server returned `404` or `500`, it throws an error immediately.
- **Step 4:** Calls `await response.json()` to parse the incoming text into a JavaScript object (`data`).
- **Step 5 & 6:** Injects the values (`data.name`, `data.branch`, etc.) into the respective DOM elements and reveals the table (`studentDisplay.style.display = "block"`).
- **Step 7 (`catch`):** If the server is offline or fails, it catches the exception and renders a clear error notification in `#errorMessage`.
- **Step 8 (`finally`):** Re-enables the button (`fetchBtn.disabled = false`) so the user can click again, even if an error occurred.

#### Block 4: Event Listener Attachment
```javascript
fetchBtn.addEventListener("click", fetchStudentData);
```
- Binds `fetchStudentData` to the click event of the **Fetch Data** button.

---

## Part 3: Step-by-Step Request Tracing

### First Request (Initial Click)
1. **Initial State:** `requestCount` on server = `0`. In browser, table is hidden.
2. **User action:** User clicks **Fetch Data**.
3. **Browser:** Shows loading text, disables button, dispatches `GET /api/student`.
4. **Server:** Receives request.
   - `requestCount` changes from `0` to `1`.
   - `timestamp` generated: e.g. `"5:30:00 PM"`.
   - Terminal logs: `GET /api/student: request 1`.
   - Server returns:
     ```json
     {
       "name": "Student Name",
       "branch": "CSE",
       "year": "3rd Year",
       "requestNumber": 1,
       "timestamp": "5:30:00 PM"
     }
     ```
5. **Browser:** Receives JSON, populates table cells, displays Request `#1`, displays `"5:30:00 PM"`, reveals the table, and re-enables the button.

### Second Request (Subsequent Click)
1. **Initial State:** `requestCount` on server = `1`. In browser, Request `#1` is currently displayed.
2. **User action:** User clicks **Fetch Data** a second time.
3. **Browser:** Sends a brand new `GET /api/student` request over HTTP.
4. **Server:** Receives request.
   - `requestCount` increments from `1` to `2`.
   - `timestamp` generated: e.g. `"5:30:05 PM"`.
   - Terminal logs: `GET /api/student: request 2`.
   - Server returns updated JSON with `"requestNumber": 2`.
5. **Browser:** Updates `#requestNumber` to `#2` and updates `#fetchTimestamp` to `"5:30:05 PM"`.

---

## Part 4: Failure Scenarios & Error Handling

What happens if the Express server is stopped while the webpage is open?
1. The user clicks **Fetch Data**.
2. The browser tries to connect to `http://localhost:3001/api/student`.
3. Because the port is closed, the browser's network stack rejects the promise with a `TypeError: Failed to fetch`.
4. The `catch (err)` block catches this error:
   - Sets `errorMessage.textContent` to `"Failed to fetch data: Failed to fetch. Ensure the Express server is running on port 3001."`.
   - Sets `errorMessage.style.display = "block"`.
5. The `finally` block runs, hiding the loading indicator and re-enabling the button. The application does not crash.

---

## Part 5: Impact of Changing Values

Suppose in `server.js` you change:
```javascript
const studentData = {
  name: "Alex Morgan",
  branch: "Artificial Intelligence & Data Science",
  year: "Final Year"
};
```
- Next time you restart the server and click **Fetch Data**, the browser table instantly reflects the updated values without requiring any changes to `index.html`.
- This highlights the decoupling of frontend representation and backend data sources.
