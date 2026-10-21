/**
 * Assignment 6 — Requirement 4
 * $match then $group: Count students scoring above 60 in each branch
 *
 * Demonstrates:
 * 1. $match stage: Filters students where overall marks > 60.
 * 2. $group stage: Groups remaining documents by "branch" and counts them ($sum: 1).
 * 3. $project stage: Renames _id to branch and projects studentCount.
 * 4. $sort stage: Orders by branch name ascending.
 * 5. Display formatted results using console.table().
 *
 * Note: Uses the overall "marks" field, as required.
 */

const { MongoClient } = require("mongodb");

const MONGODB_URI = process.env.MONGODB_URI || "mongodb://127.0.0.1:27017/waf_assignment_6";
const DB_NAME = "waf_assignment_6";

async function runBranchAbove60() {
  const client = new MongoClient(MONGODB_URI, { serverSelectionTimeoutMS: 3000 });

  try {
    await client.connect();
    const db = client.db(DB_NAME);
    const studentsCol = db.collection("students");

    console.log("================================================================================");
    console.log("Requirement 4: MongoDB Aggregation — $match & $group (Students with Marks > 60)");
    console.log("================================================================================\n");

    const pipeline = [
      // Stage 1: Filter students whose overall marks are strictly greater than 60
      {
        $match: {
          marks: { $gt: 60 }
        }
      },
      // Stage 2: Group by branch and accumulate count
      {
        $group: {
          _id: "$branch",
          studentsAbove60Count: { $sum: 1 }
        }
      },
      // Stage 3: Clean projection
      {
        $project: {
          _id: 0,
          branch: "$_id",
          studentsAbove60Count: 1
        }
      },
      // Stage 4: Sort alphabetically by branch
      {
        $sort: { branch: 1 }
      }
    ];

    const results = await studentsCol.aggregate(pipeline).toArray();

    if (results.length === 0) {
      console.log("No students scoring above 60 found. Please run 'npm run seed' first.");
    } else {
      console.log(`Branch-wise count of students scoring > 60:\n`);
      console.table(results);
    }

    console.log("\nPipeline stages executed:");
    console.log("1. $match   : Filtered documents with condition { marks: { $gt: 60 } }");
    console.log("2. $group   : Grouped by '$branch' and computed count with { $sum: 1 }");
    console.log("3. $project : Reshaped _id to branch and projected studentsAbove60Count");
    console.log("4. $sort    : Sorted by branch ascending");
    console.log("================================================================================");

    return results;

  } catch (err) {
    console.error("\n[BRANCH ABOVE 60 ERROR]", err.message);
    if (err.message.includes("ECONNREFUSED") || err.name === "MongoServerSelectionError") {
      console.error("\nCould not connect to MongoDB. Please ensure your MongoDB Community Server is running.");
      console.error("Default connection URI: mongodb://127.0.0.1:27017/waf_assignment_6");
      console.error("To start MongoDB on Windows: net start MongoDB (or run mongod.exe)");
    }
    process.exitCode = 1;
  } finally {
    await client.close();
  }
}

if (require.main === module) {
  runBranchAbove60();
}

module.exports = { runBranchAbove60 };
