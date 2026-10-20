/**
 * Assignment 4 — Practical 1: Express Server & Browser Fetch
 * A beginner-friendly Express.js server that serves static HTML
 * and provides an API endpoint to return student information as JSON.
 */

const express = require("express");
const path = require("path");

const app = express();
const PORT = process.env.PORT || 3000;

// 1. Middleware: Serve static files from the "public" directory
app.use(express.static(path.join(__dirname, "public")));

// 2. Hardcoded Student Data (simulating a database record)
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

// 3. API Endpoint: GET /api/student
// Returns student information as a JSON response
app.get("/api/student", (req, res) => {
  const timestamp = new Date().toLocaleTimeString();
  console.log(`[EXPRESS SERVER ${timestamp}] Received GET request for /api/student`);

  // Send the studentData object as JSON
  res.json(studentData);
});

// 4. Default Route: Serve the main index.html file
app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "index.html"));
});

// 5. Start the server
app.listen(PORT, () => {
  console.log("==================================================");
  console.log(`🚀 Express Server is running!`);
  console.log(`🌐 Open in browser: http://localhost:${PORT}`);
  console.log(`📡 API endpoint:    http://localhost:${PORT}/api/student`);
  console.log("==================================================");
});
