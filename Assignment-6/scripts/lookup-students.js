/**
 * Assignment 6 — Requirement 1
 * $lookup: Join students with departments
 *
 * Demonstrates:
 * 1. $lookup stage to join "students" collection with "departments" on student.departmentId == department._id.
 * 2. $unwind stage to flatten the single-element departmentDetails array into an object.
 * 3. $project stage to shape output: name, rollNo, branch, departmentName, hod.
 * 4. $sort stage by rollNo ascending.
 * 5. Display formatted results using console.table().
 */

const { MongoClient } = require("mongodb");

const MONGODB_URI = process.env.MONGODB_URI || "mongodb://127.0.0.1:27017/waf_lab";
const DB_NAME = "waf_lab";

async function runLookup() {
  const client = new MongoClient(MONGODB_URI, { serverSelectionTimeoutMS: 3000 });

  try {
    await client.connect();
    const db = client.db(DB_NAME);
    const studentsCol = db.collection("students");

    console.log("================================================================================");
    console.log("Requirement 1: MongoDB Aggregation — $lookup Join (Students + Departments)");
    console.log("================================================================================\n");

    const pipeline = [
      // Stage 1: Perform left outer join with departments collection
      {
        $lookup: {
          from: "departments",
          localField: "departmentId",
          foreignField: "_id",
          as: "departmentDetails"
        }
      },
      // Stage 2: Flatten the departmentDetails array into a single sub-document
      {
        $unwind: {
          path: "$departmentDetails",
          preserveNullAndEmptyArrays: false // Only include students with a valid matched department
        }
      },
      // Stage 3: Project the required fields cleanly
      {
        $project: {
          _id: 0,
          rollNo: "$rollNo",
          name: "$name",
          branch: "$branch",
          departmentName: "$departmentDetails.name",
          hod: "$departmentDetails.hod"
        }
      },
      // Stage 4: Order deterministically by roll number
      {
        $sort: { rollNo: 1 }
      }
    ];

    const results = await studentsCol.aggregate(pipeline).toArray();

    if (results.length === 0) {
      console.log("No student records found. Please run 'npm run seed' first to insert sample data.");
    } else {
      console.log(`Found ${results.length} students joined with department details:\n`);
      console.table(results);
    }

    console.log("\nPipeline stages executed:");
    console.log("1. $lookup  : Joined students.departmentId -> departments._id");
    console.log("2. $unwind  : Deconstructed $departmentDetails array to object");
    console.log("3. $project : Extracted rollNo, name, branch, departmentName, hod");
    console.log("4. $sort    : Sorted by rollNo ascending");
    console.log("================================================================================");

    return results;

  } catch (err) {
    console.error("\n[LOOKUP ERROR]", err.message);
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
  runLookup();
}

module.exports = { runLookup };
