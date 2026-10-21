/**
 * Assignment 6 — Requirement 3
 * $unwind and $group: Total and average subject marks per student
 *
 * Demonstrates:
 * 1. $unwind stage to deconstruct the "subjects" array into individual documents.
 * 2. $group stage grouped by student identity (_id: { rollNo, name }).
 * 3. Accumulators:
 *    - $sum: "$subjects.marks" for total subject marks.
 *    - $avg: "$subjects.marks" for average subject marks.
 *    - $sum: 1 for counting subjects.
 * 4. $project stage to round average to 2 decimal places and flatten keys.
 * 5. $sort stage by rollNo ascending.
 * 6. Display formatted results using console.table().
 *
 * Note: Calculates from the nested "subjects" array, NOT the overall "marks" field.
 */

const { MongoClient } = require("mongodb");

const MONGODB_URI = process.env.MONGODB_URI || "mongodb://127.0.0.1:27017/waf_assignment_6";
const DB_NAME = "waf_assignment_6";

async function runSubjectSummary() {
  const client = new MongoClient(MONGODB_URI, { serverSelectionTimeoutMS: 3000 });

  try {
    await client.connect();
    const db = client.db(DB_NAME);
    const studentsCol = db.collection("students");

    console.log("================================================================================");
    console.log("Requirement 3: MongoDB Aggregation — $unwind & $group (Subject Marks Summary)");
    console.log("================================================================================\n");

    const pipeline = [
      // Stage 1: Deconstruct subjects array into separate documents
      {
        $unwind: "$subjects"
      },
      // Stage 2: Group by student rollNo and name
      {
        $group: {
          _id: {
            rollNo: "$rollNo",
            name: "$name",
            branch: "$branch"
          },
          totalSubjectMarks: { $sum: "$subjects.marks" },
          averageSubjectMarks: { $avg: "$subjects.marks" },
          subjectCount: { $sum: 1 }
        }
      },
      // Stage 3: Shape output and round average to 2 decimal places
      {
        $project: {
          _id: 0,
          rollNo: "$_id.rollNo",
          name: "$_id.name",
          branch: "$_id.branch",
          subjectCount: 1,
          totalSubjectMarks: 1,
          averageSubjectMarks: { $round: ["$averageSubjectMarks", 2] }
        }
      },
      // Stage 4: Sort by roll number ascending
      {
        $sort: { rollNo: 1 }
      }
    ];

    const results = await studentsCol.aggregate(pipeline).toArray();

    if (results.length === 0) {
      console.log("No student records found. Please run 'npm run seed' first to insert sample data.");
    } else {
      console.log(`Calculated subject summary for ${results.length} students:\n`);
      console.table(results);
    }

    console.log("\nPipeline stages executed:");
    console.log("1. $unwind  : Deconstructed $subjects array per student");
    console.log("2. $group   : Grouped by rollNo, name, branch; calculated $sum and $avg of subjects.marks");
    console.log("3. $project : Formatted fields, applied $round to 2 decimal places");
    console.log("4. $sort    : Sorted by rollNo ascending");
    console.log("================================================================================");

    return results;

  } catch (err) {
    console.error("\n[SUBJECT SUMMARY ERROR]", err.message);
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
  runSubjectSummary();
}

module.exports = { runSubjectSummary };
