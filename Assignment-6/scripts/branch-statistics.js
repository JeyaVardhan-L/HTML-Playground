/**
 * Assignment 6 — Requirement 5
 * Branch-wise average, maximum and minimum marks
 *
 * Demonstrates:
 * 1. $group stage: Groups documents by "branch".
 * 2. Accumulators:
 *    - $avg: "$marks" for average overall marks.
 *    - $max: "$marks" for maximum overall marks.
 *    - $min: "$marks" for minimum overall marks.
 *    - $sum: 1 for student count in each branch.
 * 3. $project stage: Shapes fields and rounds average to 2 decimal places.
 * 4. $sort stage: Orders by averageMarks descending (-1).
 * 5. Display formatted results using console.table().
 *
 * Note: Uses the overall "marks" field, as required.
 */

const { MongoClient } = require("mongodb");

const MONGODB_URI = process.env.MONGODB_URI || "mongodb://127.0.0.1:27017/waf_lab";
const DB_NAME = "waf_lab";

async function runBranchStatistics() {
  const client = new MongoClient(MONGODB_URI, { serverSelectionTimeoutMS: 3000 });

  try {
    await client.connect();
    const db = client.db(DB_NAME);
    const studentsCol = db.collection("students");

    console.log("================================================================================");
    console.log("Requirement 5: MongoDB Aggregation — Branch-Wise Statistics ($avg, $max, $min)");
    console.log("================================================================================\n");

    const pipeline = [
      // Stage 1: Group by branch and calculate accumulators
      {
        $group: {
          _id: "$branch",
          averageMarks: { $avg: "$marks" },
          maxMarks: { $max: "$marks" },
          minMarks: { $min: "$marks" },
          totalStudents: { $sum: 1 }
        }
      },
      // Stage 2: Shape fields and round average to 2 decimal places
      {
        $project: {
          _id: 0,
          branch: "$_id",
          totalStudents: 1,
          averageMarks: { $round: ["$averageMarks", 2] },
          maxMarks: 1,
          minMarks: 1
        }
      },
      // Stage 3: Sort by averageMarks descending (highest performing branch first)
      {
        $sort: { averageMarks: -1 }
      }
    ];

    const results = await studentsCol.aggregate(pipeline).toArray();

    if (results.length === 0) {
      console.log("No student records found. Please run 'npm run seed' first to insert sample data.");
    } else {
      console.log(`Branch statistics calculated across ${results.length} branches (sorted by avg desc):\n`);
      console.table(results);
    }

    console.log("\nPipeline stages executed:");
    console.log("1. $group   : Grouped by '$branch'; calculated $avg, $max, $min, and $sum(1)");
    console.log("2. $project : Formatted fields, applied $round to averageMarks (2 decimal places)");
    console.log("3. $sort    : Sorted by averageMarks: -1 (descending)");
    console.log("================================================================================");

    return results;

  } catch (err) {
    console.error("\n[BRANCH STATISTICS ERROR]", err.message);
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
  runBranchStatistics();
}

module.exports = { runBranchStatistics };
