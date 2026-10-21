/**
 * Assignment 7 — Requirement 8
 * Delete all students whose marks are less than 40
 *
 * Demonstrates:
 * 1. The deleteMany() method using a query filter: { marks: { $lt: 40 } }.
 * 2. Pre-deletion warning and preview of qualifying records.
 * 3. Interactive confirmation prompt (using readline) to prevent accidental data loss.
 * 4. Non-interactive bypass flag: --confirm, --yes, or -y (for automated testing).
 * 5. Displaying the exact count of deleted documents.
 * 6. Guidance on restoring data via 'npm run seed'.
 *
 * CAUTION: Destructive operation. Affects only documents where marks < 40.
 */

const { MongoClient } = require("mongodb");
const readline = require("readline");

const MONGODB_URI = process.env.MONGODB_URI || "mongodb://127.0.0.1:27017/waf_assignment_7";
const DB_NAME = "waf_assignment_7";

// Helper to ask for interactive user confirmation
function askConfirmation(question) {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });

  return new Promise((resolve) => {
    rl.question(question, (answer) => {
      rl.close();
      resolve(answer.trim().toLowerCase());
    });
  });
}

async function runDeleteBelow40() {
  const client = new MongoClient(MONGODB_URI, { serverSelectionTimeoutMS: 3000 });

  // Check for non-interactive confirmation flags: --confirm, --yes, -y
  const args = process.argv.slice(2);
  const autoConfirmed = args.some(arg => ["--confirm", "--yes", "-y"].includes(arg.toLowerCase()));

  try {
    await client.connect();
    const db = client.db(DB_NAME);
    const studentsCol = db.collection("students");

    console.log("================================================================================");
    console.log("Requirement 8: MongoDB Destructive Delete — deleteMany({ marks: { $lt: 40 } })");
    console.log("================================================================================\n");

    const filter = { marks: { $lt: 40 } };

    // 1. Preview documents that match the deletion filter before deleting
    const candidates = await studentsCol.find(filter).project({ _id: 0, rollNo: 1, name: 1, branch: 1, marks: 1 }).toArray();

    console.log("-------------------------------- WARNING ---------------------------------------");
    console.log("Target Database    : " + DB_NAME);
    console.log("Target Collection  : students");
    console.log("Filter Condition   : { marks: { $lt: 40 } }");
    console.log(`Matching Documents : ${candidates.length} record(s) found eligible for deletion.`);
    console.log("--------------------------------------------------------------------------------\n");

    if (candidates.length === 0) {
      console.log("No students currently have marks below 40.");
      console.log("(If you ran this script earlier, run 'npm run seed' to restore sample student records.)");
      return { deletedCount: 0 };
    }

    console.log("Records that will be PERMANENTLY deleted:");
    console.table(candidates);

    // 2. Obtain explicit confirmation if not bypassed via CLI flag
    if (!autoConfirmed) {
      const response = await askConfirmation("\nAre you SURE you want to delete these records? Type 'yes' to proceed: ");
      if (response !== "yes" && response !== "y") {
        console.log("\n[ABORTED] Deletion cancelled by user. No records were deleted.");
        return { deletedCount: 0, aborted: true };
      }
    } else {
      console.log("\n[AUTO-CONFIRMED] Non-interactive flag detected. Proceeding with deletion...");
    }

    // 3. Execute deleteMany()
    const deleteResult = await studentsCol.deleteMany(filter);

    console.log("\n================================================================================");
    console.log(`✓ DELETION COMPLETE: Successfully deleted ${deleteResult.deletedCount} student record(s).`);
    console.log("================================================================================");

    // 4. Verify remaining student count
    const remainingCount = await studentsCol.countDocuments();
    console.log(`Remaining students in collection: ${remainingCount}`);
    console.log("\nTo RESTORE the deleted sample records at any time, run:");
    console.log("  npm run seed");
    console.log("================================================================================\n");

    return deleteResult;

  } catch (err) {
    console.error("\n[DELETE-BELOW-40 ERROR]", err.message);
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
  runDeleteBelow40();
}

module.exports = { runDeleteBelow40 };
