/**
 * Assignment 6 — Requirement 2
 * Express REST API using the native MongoDB Node.js driver
 *
 * Routes implemented:
 * - POST   /students          -> Add a new student (validates rollNo, name, marks)
 * - GET    /students          -> List all students
 * - GET    /students/:rollNo  -> Retrieve one student by roll number
 * - PUT    /students/:rollNo  -> Update an existing student (preserves _id)
 * - DELETE /students/:rollNo  -> Delete a student by roll number
 *
 * Configuration:
 * - PORT: 3002 (prevents conflict with Assignment 4 & 5 ports)
 * - MONGODB_URI: defaults to mongodb://127.0.0.1:27017/waf_assignment_6
 * - DB_NAME: waf_assignment_6
 */

const express = require("express");
const { MongoClient, ObjectId } = require("mongodb");

const app = express();
const PORT = process.env.PORT || 3002;
const MONGODB_URI = process.env.MONGODB_URI || "mongodb://127.0.0.1:27017/waf_assignment_6";
const DB_NAME = "waf_assignment_6";

// Middleware to parse incoming JSON request bodies
app.use(express.json());

// MongoDB client instance & reference to collections
let client;
let db;
let studentsCol;

/**
 * Health check / Root documentation route
 */
app.get("/", (req, res) => {
  res.json({
    message: "WAF Lab Assignment 6 — Student REST API (Express + MongoDB)",
    database: DB_NAME,
    port: PORT,
    endpoints: [
      { method: "GET", path: "/students", description: "List all students" },
      { method: "GET", path: "/students/:rollNo", description: "Get student by roll number" },
      { method: "POST", path: "/students", description: "Create a new student" },
      { method: "PUT", path: "/students/:rollNo", description: "Update student by roll number" },
      { method: "DELETE", path: "/students/:rollNo", description: "Delete student by roll number" }
    ]
  });
});

/**
 * 1. POST /students — Add a new student
 * Status Codes:
 * - 201 Created: Student added successfully
 * - 400 Bad Request: Missing rollNo or name, invalid marks, or duplicate rollNo
 * - 500 Internal Server Error: Database failure
 */
app.post("/students", async (req, res) => {
  try {
    const { rollNo, name, branch, departmentId, marks, subjects } = req.body;

    // Validation: rollNo and name are strictly required non-empty strings
    if (!rollNo || typeof rollNo !== "string" || rollNo.trim() === "") {
      return res.status(400).json({ error: "Validation failed: 'rollNo' is required and must be a non-empty string." });
    }

    if (!name || typeof name !== "string" || name.trim() === "") {
      return res.status(400).json({ error: "Validation failed: 'name' is required and must be a non-empty string." });
    }

    // Validation: marks must be numeric if provided
    if (marks !== undefined && (typeof marks !== "number" || isNaN(marks) || marks < 0 || marks > 100)) {
      return res.status(400).json({ error: "Validation failed: 'marks' must be a valid number between 0 and 100." });
    }

    // Validation: subjects must be an array if provided
    if (subjects !== undefined && !Array.isArray(subjects)) {
      return res.status(400).json({ error: "Validation failed: 'subjects' must be an array of objects." });
    }

    // Check for existing student with same rollNo to return clean 400
    const existing = await studentsCol.findOne({ rollNo: rollNo.trim() });
    if (existing) {
      return res.status(400).json({ error: `Duplicate key: A student with roll number '${rollNo}' already exists.` });
    }

    // Convert departmentId to ObjectId if valid string provided
    let parsedDeptId = null;
    if (departmentId) {
      if (ObjectId.isValid(departmentId)) {
        parsedDeptId = new ObjectId(departmentId);
      } else {
        return res.status(400).json({ error: "Validation failed: 'departmentId' is not a valid 24-character hexadecimal ObjectId." });
      }
    }

    const newStudent = {
      rollNo: rollNo.trim(),
      name: name.trim(),
      branch: branch ? branch.trim() : "Unassigned",
      departmentId: parsedDeptId,
      marks: marks !== undefined ? marks : 0,
      subjects: subjects || []
    };

    const result = await studentsCol.insertOne(newStudent);

    return res.status(201).json({
      message: "Student created successfully",
      student: { _id: result.insertedId, ...newStudent }
    });

  } catch (err) {
    // Catch MongoDB duplicate key error (code 11000) as additional safety
    if (err.code === 11000) {
      return res.status(400).json({ error: "Duplicate key: A student with this roll number already exists." });
    }
    console.error("[POST /students error]", err);
    return res.status(500).json({ error: "Internal server error while creating student." });
  }
});

/**
 * 2. GET /students — List all students
 * Status Codes:
 * - 200 OK: Array of student documents
 * - 500 Internal Server Error: Database failure
 */
app.get("/students", async (req, res) => {
  try {
    const students = await studentsCol.find({}).sort({ rollNo: 1 }).toArray();
    return res.status(200).json(students);
  } catch (err) {
    console.error("[GET /students error]", err);
    return res.status(500).json({ error: "Internal server error while fetching students." });
  }
});

/**
 * 3. GET /students/:rollNo — Retrieve one student by roll number
 * Status Codes:
 * - 200 OK: Matching student document
 * - 404 Not Found: No student matches the given roll number
 * - 500 Internal Server Error: Database failure
 */
app.get("/students/:rollNo", async (req, res) => {
  try {
    const { rollNo } = req.params;
    const student = await studentsCol.findOne({ rollNo: rollNo.trim() });

    if (!student) {
      return res.status(404).json({ error: `Student with roll number '${rollNo}' was not found.` });
    }

    return res.status(200).json(student);
  } catch (err) {
    console.error("[GET /students/:rollNo error]", err);
    return res.status(500).json({ error: "Internal server error while retrieving student." });
  }
});

/**
 * 4. PUT /students/:rollNo — Update an existing student's fields
 * Status Codes:
 * - 200 OK: Student updated successfully
 * - 400 Bad Request: Validation failed or attempted immutable field modification
 * - 404 Not Found: No student found with given roll number
 * - 500 Internal Server Error: Database failure
 */
app.put("/students/:rollNo", async (req, res) => {
  try {
    const { rollNo } = req.params;
    const updates = { ...req.body };

    // Disallow modifying MongoDB internal _id
    if (updates._id !== undefined) {
      delete updates._id;
    }

    // Disallow empty update payload
    if (Object.keys(updates).length === 0) {
      return res.status(400).json({ error: "No fields provided for update." });
    }

    // Validate marks if provided in update
    if (updates.marks !== undefined && (typeof updates.marks !== "number" || isNaN(updates.marks) || updates.marks < 0 || updates.marks > 100)) {
      return res.status(400).json({ error: "Validation failed: 'marks' must be a valid number between 0 and 100." });
    }

    // Validate departmentId if provided
    if (updates.departmentId !== undefined) {
      if (ObjectId.isValid(updates.departmentId)) {
        updates.departmentId = new ObjectId(updates.departmentId);
      } else {
        return res.status(400).json({ error: "Validation failed: 'departmentId' is not a valid 24-character hexadecimal ObjectId." });
      }
    }

    // Validate rollNo if changed in body (must not collide with another student)
    if (updates.rollNo && updates.rollNo !== rollNo) {
      const collision = await studentsCol.findOne({ rollNo: updates.rollNo });
      if (collision) {
        return res.status(400).json({ error: `Cannot change roll number: roll number '${updates.rollNo}' is already taken.` });
      }
    }

    const result = await studentsCol.findOneAndUpdate(
      { rollNo: rollNo.trim() },
      { $set: updates },
      { returnDocument: "after" }
    );

    if (!result) {
      return res.status(404).json({ error: `Student with roll number '${rollNo}' was not found.` });
    }

    return res.status(200).json({
      message: `Student '${rollNo}' updated successfully.`,
      student: result
    });

  } catch (err) {
    console.error("[PUT /students/:rollNo error]", err);
    return res.status(500).json({ error: "Internal server error while updating student." });
  }
});

/**
 * 5. DELETE /students/:rollNo — Delete a student by roll number
 * Status Codes:
 * - 200 OK: Student deleted successfully
 * - 404 Not Found: No student matches the given roll number
 * - 500 Internal Server Error: Database failure
 */
app.delete("/students/:rollNo", async (req, res) => {
  try {
    const { rollNo } = req.params;
    const result = await studentsCol.deleteOne({ rollNo: rollNo.trim() });

    if (result.deletedCount === 0) {
      return res.status(404).json({ error: `Student with roll number '${rollNo}' was not found.` });
    }

    return res.status(200).json({
      message: `Student '${rollNo}' was deleted successfully.`,
      deletedRollNo: rollNo.trim()
    });

  } catch (err) {
    console.error("[DELETE /students/:rollNo error]", err);
    return res.status(500).json({ error: "Internal server error while deleting student." });
  }
});

/**
 * Generic 404 handler for undefined API routes
 */
app.use((req, res) => {
  res.status(404).json({ error: `Cannot ${req.method} ${req.originalUrl}. Route not supported.` });
});

/**
 * Server startup and MongoDB connection initialization
 */
let server;

async function startServer() {
  try {
    client = new MongoClient(MONGODB_URI, { serverSelectionTimeoutMS: 3000 });
    console.log(`Connecting to MongoDB at: ${MONGODB_URI}...`);
    await client.connect();

    db = client.db(DB_NAME);
    studentsCol = db.collection("students");

    // Ensure unique index on rollNo exists on startup
    await studentsCol.createIndex({ rollNo: 1 }, { unique: true });

    server = app.listen(PORT, () => {
      console.log("==================================================");
      console.log(`Express REST API running on http://localhost:${PORT}`);
      console.log(`Connected to MongoDB Database: "${DB_NAME}"`);
      console.log(`Collection: "students" (unique index on rollNo enforced)`);
      console.log(`Ready to accept API requests.`);
      console.log("==================================================");
    });

    server.on("error", (err) => {
      if (err.code === "EADDRINUSE") {
        console.error(`\n[PORT CONFLICT] Port ${PORT} is already in use by another process.`);
        console.error(`Please stop the conflicting process or set PORT=<port> in your environment.\n`);
      } else {
        console.error("\n[SERVER ERROR]", err.message, "\n");
      }
    });

  } catch (err) {
    console.error("\n[STARTUP ERROR] Could not connect to MongoDB:", err.message);
    if (err.message.includes("ECONNREFUSED") || err.name === "MongoServerSelectionError") {
      console.error("Please ensure MongoDB Community Server is started on port 27017.");
      console.error("To start MongoDB on Windows: net start MongoDB (or run mongod.exe)");
    }
    process.exit(1);
  }
}

/**
 * Graceful shutdown handlers
 */
async function shutdown(signal) {
  console.log(`\nReceived ${signal}. Shutting down gracefully...`);
  if (server) {
    server.close(() => {
      console.log("HTTP server closed.");
    });
  }
  if (client) {
    try {
      await client.close();
      console.log("MongoDB connection closed.");
    } catch (err) {
      console.error("Error closing MongoDB connection:", err.message);
    }
  }
  process.exit(0);
}

process.on("SIGINT", () => shutdown("SIGINT"));
process.on("SIGTERM", () => shutdown("SIGTERM"));

if (require.main === module) {
  startServer();
}

module.exports = { app, startServer };
