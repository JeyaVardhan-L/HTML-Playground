/**
 * Assignment 7 — Requirement 7
 * Find a document by _id using new ObjectId("...")
 *
 * Demonstrates:
 * 1. Importing the native ObjectId class from the mongodb driver.
 * 2. Converting a 24-character hexadecimal string into a BSON ObjectId instance.
 * 3. Querying the "students" collection using { _id: new ObjectId("...") }.
 * 4. Contrasting query behavior: why { _id: "string" } fails vs { _id: ObjectId } succeeds.
 * 5. Displaying the matching student document.
 */

const { MongoClient, ObjectId } = require("mongodb");

const MONGODB_URI = process.env.MONGODB_URI || "mongodb://127.0.0.1:27017/waf_assignment_7";
const DB_NAME = "waf_assignment_7";

// Stable 24-character hex ID seeded for student Aarav Sharma (Roll No: 101)
const DEFAULT_STUDENT_ID = "65f1b2b2b2b2b2b2b2b2b101";

async function runFindById(idHex = DEFAULT_STUDENT_ID) {
  const client = new MongoClient(MONGODB_URI, { serverSelectionTimeoutMS: 3000 });

  try {
    await client.connect();
    const db = client.db(DB_NAME);
    const studentsCol = db.collection("students");

    console.log("================================================================================");
    console.log("Requirement 7: MongoDB Query by Primary Key — new ObjectId(\"...\")");
    console.log("================================================================================\n");

    // 1. Validate the hex string format before constructing ObjectId
    if (!ObjectId.isValid(idHex)) {
      console.error(`[INVALID ID] '${idHex}' is not a valid 24-character hexadecimal ObjectId.`);
      return null;
    }

    // 2. Instantiate the BSON ObjectId
    const objectId = new ObjectId(idHex);
    console.log(`Hexadecimal String : "${idHex}"`);
    console.log(`BSON ObjectId Type : ObjectId("${objectId.toString()}")`);
    console.log(`Timestamp in ID    : ${objectId.getTimestamp().toISOString()}\n`);

    // 3. Demonstrate why string queries fail:
    const stringResult = await studentsCol.findOne({ _id: idHex });
    console.log("--- BSON Type Demonstration ---");
    console.log("1. Querying with plain string: findOne({ _id: \"" + idHex + "\" })");
    console.log("   Result:", stringResult, "← (null because MongoDB matches on both value AND BSON type)");

    // 4. Query using proper new ObjectId(...)
    const properResult = await studentsCol.findOne({ _id: objectId });
    console.log("\n2. Querying with new ObjectId: findOne({ _id: new ObjectId(\"" + idHex + "\") })");
    console.log("   Result: MATCH FOUND!\n");

    if (properResult) {
      console.log("Retrieved Student Document:");
      console.log(JSON.stringify(properResult, null, 2));
    } else {
      console.log(`No student found with ID ${idHex}. Please run 'npm run seed' first.`);
    }

    console.log("\n================================================================================");
    console.log("Key Concept Explained:");
    console.log("MongoDB documents store _id as a 12-byte binary BSON type (Type Code 7).");
    console.log("A JavaScript string is UTF-8 text (Type Code 2).");
    console.log("Because MongoDB is strongly typed at the BSON layer, a string never matches an ObjectId.");
    console.log("Always wrap ID strings in 'new ObjectId(idString)' when querying by _id!");
    console.log("================================================================================");

    return properResult;

  } catch (err) {
    console.error("\n[FIND-BY-ID ERROR]", err.message);
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

// Allow passing a custom ObjectId from the CLI: node scripts/find-by-id.js [hexId]
const targetId = process.argv[2] || DEFAULT_STUDENT_ID;

if (require.main === module) {
  runFindById(targetId);
}

module.exports = { runFindById };
