/**
 * Assignment 7 — Requirement 6
 * Top three scorers using MongoDB cursor methods sort() and limit()
 *
 * Demonstrates:
 * 1. Querying the "students" collection.
 * 2. Using the native cursor method .sort({ marks: -1, rollNo: 1 }):
 *    - marks: -1 (descending order by overall score)
 *    - rollNo: 1 (deterministic ascending tie-breaker)
 * 3. Using the native cursor method .limit(3) to restrict the result set to 3 documents.
 * 4. Projecting relevant fields: rollNo, name, branch, marks.
 * 5. Display formatted results using console.table().
 *
 * Note: Uses real MongoDB cursor operators, not an in-memory JavaScript array sort.
 */

const { MongoClient } = require("mongodb");

const MONGODB_URI = process.env.MONGODB_URI || "mongodb://127.0.0.1:27017/waf_lab";
const DB_NAME = "waf_lab";

async function runTopThree() {
  const client = new MongoClient(MONGODB_URI, { serverSelectionTimeoutMS: 3000 });

  try {
    await client.connect();
    const db = client.db(DB_NAME);
    const studentsCol = db.collection("students");

    console.log("================================================================================");
    console.log("Requirement 6: MongoDB Cursor Methods — sort() and limit() (Top 3 Scorers)");
    console.log("================================================================================\n");

    // Execute query using native MongoDB cursor methods: sort() and limit()
    const topStudents = await studentsCol
      .find({})
      .project({ _id: 0, rollNo: 1, name: 1, branch: 1, marks: 1 })
      .sort({ marks: -1, rollNo: 1 })
      .limit(3)
      .toArray();

    if (topStudents.length === 0) {
      console.log("No student records found. Please run 'npm run seed' first to insert sample data.");
    } else {
      console.log("Top 3 student scorers retrieved directly via MongoDB cursor:\n");
      console.table(topStudents);
    }

    console.log("\nCursor methods executed on MongoDB server:");
    console.log("1. find({})                     : Scans students collection");
    console.log("2. sort({ marks: -1, rollNo: 1 }): Orders by marks descending with rollNo tie-breaker");
    console.log("3. limit(3)                     : Stops cursor evaluation after 3 qualifying documents");
    console.log("4. project({ ... })             : Transferred only required fields across the network");
    console.log("================================================================================");

    return topStudents;

  } catch (err) {
    console.error("\n[TOP-THREE ERROR]", err.message);
    if (err.message.includes("ECONNREFUSED") || err.name === "MongoServerSelectionError") {
      console.error("\nCould not connect to MongoDB. Please ensure your MongoDB Community Server is running.");
      console.error("Default connection URI: mongodb://127.0.0.1:27017/waf_lab");
      console.error("To start MongoDB on Windows: net start MongoDB (or run mongod.exe)");
    }
    process.exitCode = 1;
  } finally {
    await client.close();
  }
}

if (require.main === module) {
  runTopThree();
}

module.exports = { runTopThree };
