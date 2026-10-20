/**
 * Assignment 5: Fetching the data with a new connection using Express js
 *
 * Demonstrates:
 * 1. Serving static files from the "public" directory.
 * 2. Providing an API endpoint (GET /api/student).
 * 3. Maintaining a server-side request counter that increments on every request.
 * 4. Generating a fresh server-side timestamp for each incoming request.
 * 5. Logging each request to the terminal in a clear, numbered format.
 */

const express = require("express");
const path = require("path");

const app = express();
const PORT = 3001;

// 1. Server-side request counter initialized to zero
let requestCount = 0;

// 2. Sample student data stored in a simple JavaScript object
const studentData = {
  name: "Student Name",
  branch: "CSE",
  year: "3rd Year"
};

// 3. Middleware to serve static files from the "public" directory
app.use(express.static(path.join(__dirname, "public")));

// 4. API Endpoint: GET /api/student
// Every request increments the counter, creates a fresh timestamp, and returns dynamic JSON
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
