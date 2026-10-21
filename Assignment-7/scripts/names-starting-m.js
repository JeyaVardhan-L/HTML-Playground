/**
 * Assignment 7 — Requirement 9
 * Search student names starting with 'M' using MongoDB $regex
 *
 * Demonstrates:
 * 1. Performing pattern matching directly on the database engine using $regex.
 * 2. Regular expression pattern: "^M" (or /^m/i):
 *    - '^' anchors matching to the beginning of the string.
 *    - 'M' matches the character M.
 *    - $options: "i" enables case-insensitivity (matches 'M' and 'm').
 * 3. Display matching students: rollNo, name, branch, marks.
 *
 * Note: Query is evaluated inside MongoDB, not filtered in-memory with JS array methods.
 */

const { MongoClient } = require("mongodb");

const MONGODB_URI = process.env.MONGODB_URI || "mongodb://127.0.0.1:27017/waf_assignment_7";
const DB_NAME = "waf_assignment_7";

async function runNamesStartingM() {
  const client = new MongoClient(MONGODB_URI, { serverSelectionTimeoutMS: 3000 });

  try {
    await client.connect();
    const db = client.db(DB_NAME);
    const studentsCol = db.collection("students");

    console.log("================================================================================");
    console.log("Requirement 9: MongoDB Pattern Matching — $regex (Names Starting with 'M')");
    console.log("================================================================================\n");

    // Query filter with $regex and case-insensitive option
    const query = {
      name: {
        $regex: "^M",
        $options: "i" // Case-insensitive flag
      }
    };

    console.log("Query Filter Object:", JSON.stringify(query, null, 2));
    console.log("Regex Explanation  : '^' = starts with, 'M' = letter M, 'i' = case-insensitive\n");

    const matchingStudents = await studentsCol
      .find(query)
      .project({ _id: 0, rollNo: 1, name: 1, branch: 1, marks: 1 })
      .sort({ name: 1 })
      .toArray();

    if (matchingStudents.length === 0) {
      console.log("No students found with names starting with 'M'. Please run 'npm run seed' first.");
    } else {
      console.log(`Found ${matchingStudents.length} student(s) matching /^M/i:\n`);
      console.table(matchingStudents);
    }

    console.log("\n================================================================================");
    console.log("Execution Details:");
    console.log("Filter sent to MongoDB: { name: { $regex: '^M', $options: 'i' } }");
    console.log("Evaluation executed inside database engine; only matching rows returned.");
    console.log("================================================================================");

    return matchingStudents;

  } catch (err) {
    console.error("\n[NAMES-STARTING-M ERROR]", err.message);
    if (err.message.includes("ECONNREFUSED") || err.name === "MongoServerSelectionError") {
      console.error("\nCould not connect to MongoDB. Please ensure your MongoDB Community Server is running.");
      console.error("Default connection URI: mongodb://127.0.0.1:27017/waf_assignment_7");
      console.error("To start MongoDB on Windows: net start MongoDB (or run mongod.exe)");
    }
    process.exitCode = 1;
  } finally {
    await client.close();
  }
}

if (require.main === module) {
  runNamesStartingM();
}

module.exports = { runNamesStartingM };
