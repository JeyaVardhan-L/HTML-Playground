/**
 * Assignment 6: Seed Script for MongoDB Database (waf_assignment_6)
 *
 * Idempotently seeds:
 * 1. "departments" collection with 3 distinct departments (CSE, ECE, EEE)
 * 2. "students" collection with 8 realistic student records
 *
 * Characteristics of sample data:
 * - 3 branches: CSE, ECE, EEE
 * - Marks distribution: scores above 60 (Aarav, Meera, Pooja, Manish, Vikram, Neha)
 * - Scores below 40: Rohan (35), Suresh (38)
 * - Top 3 candidates: Meera (94), Pooja (91), Aarav (88)
 * - Names starting with 'M': Meera Nair, Manish Gupta
 * - Distinct branch averages, maximums, and minimums
 * - Deterministic ObjectIds for 100% reproducible testing
 */

const { MongoClient, ObjectId } = require("mongodb");

const MONGODB_URI = process.env.MONGODB_URI || "mongodb://127.0.0.1:27017/waf_assignment_6";
const DB_NAME = "waf_assignment_6";

// Stable Department ObjectIds
const DEPT_IDS = {
  CSE: new ObjectId("65f1a1a1a1a1a1a1a1a1a101"),
  ECE: new ObjectId("65f1a1a1a1a1a1a1a1a1a102"),
  EEE: new ObjectId("65f1a1a1a1a1a1a1a1a1a103")
};

const departments = [
  {
    _id: DEPT_IDS.CSE,
    name: "Computer Science & Engineering",
    hod: "Dr. K. S. Rao"
  },
  {
    _id: DEPT_IDS.ECE,
    name: "Electronics & Communication Engineering",
    hod: "Dr. P. Sharma"
  },
  {
    _id: DEPT_IDS.EEE,
    name: "Electrical & Electronics Engineering",
    hod: "Dr. R. V. Raman"
  }
];

const students = [
  {
    _id: new ObjectId("65f1b2b2b2b2b2b2b2b2b101"),
    rollNo: "101",
    name: "Aarav Sharma",
    branch: "CSE",
    departmentId: DEPT_IDS.CSE,
    marks: 88,
    subjects: [
      { name: "DBMS", marks: 90 },
      { name: "JavaScript", marks: 86 }
    ]
  },
  {
    _id: new ObjectId("65f1b2b2b2b2b2b2b2b2b102"),
    rollNo: "102",
    name: "Meera Nair",
    branch: "CSE",
    departmentId: DEPT_IDS.CSE,
    marks: 94,
    subjects: [
      { name: "DBMS", marks: 96 },
      { name: "JavaScript", marks: 92 }
    ]
  },
  {
    _id: new ObjectId("65f1b2b2b2b2b2b2b2b2b103"),
    rollNo: "103",
    name: "Rohan Varma",
    branch: "CSE",
    departmentId: DEPT_IDS.CSE,
    marks: 35,
    subjects: [
      { name: "DBMS", marks: 38 },
      { name: "JavaScript", marks: 32 }
    ]
  },
  {
    _id: new ObjectId("65f1b2b2b2b2b2b2b2b2b104"),
    rollNo: "104",
    name: "Manish Gupta",
    branch: "ECE",
    departmentId: DEPT_IDS.ECE,
    marks: 78,
    subjects: [
      { name: "Signals", marks: 82 },
      { name: "VLSI", marks: 74 }
    ]
  },
  {
    _id: new ObjectId("65f1b2b2b2b2b2b2b2b2b105"),
    rollNo: "105",
    name: "Pooja Reddy",
    branch: "ECE",
    departmentId: DEPT_IDS.ECE,
    marks: 91,
    subjects: [
      { name: "Signals", marks: 95 },
      { name: "VLSI", marks: 87 }
    ]
  },
  {
    _id: new ObjectId("65f1b2b2b2b2b2b2b2b2b106"),
    rollNo: "106",
    name: "Suresh Iyer",
    branch: "ECE",
    departmentId: DEPT_IDS.ECE,
    marks: 38,
    subjects: [
      { name: "Signals", marks: 40 },
      { name: "VLSI", marks: 36 }
    ]
  },
  {
    _id: new ObjectId("65f1b2b2b2b2b2b2b2b2b107"),
    rollNo: "107",
    name: "Vikram Das",
    branch: "EEE",
    departmentId: DEPT_IDS.EEE,
    marks: 72,
    subjects: [
      { name: "Power Systems", marks: 75 },
      { name: "Machines", marks: 69 }
    ]
  },
  {
    _id: new ObjectId("65f1b2b2b2b2b2b2b2b2b108"),
    rollNo: "108",
    name: "Neha Patel",
    branch: "EEE",
    departmentId: DEPT_IDS.EEE,
    marks: 65,
    subjects: [
      { name: "Power Systems", marks: 68 },
      { name: "Machines", marks: 62 }
    ]
  }
];

async function seedDatabase() {
  const client = new MongoClient(MONGODB_URI, { serverSelectionTimeoutMS: 3000 });

  try {
    console.log(`Connecting to MongoDB at: ${MONGODB_URI}`);
    await client.connect();
    console.log("✓ Connected successfully to MongoDB.");

    const db = client.db(DB_NAME);
    const deptCol = db.collection("departments");
    const studentsCol = db.collection("students");

    // 1. Ensure unique index on student rollNo
    await studentsCol.createIndex({ rollNo: 1 }, { unique: true });
    console.log("✓ Created/verified unique index on students(rollNo).");

    // 2. Idempotent upsert for departments
    console.log("\nSeeding departments...");
    for (const dept of departments) {
      await deptCol.updateOne(
        { _id: dept._id },
        { $set: dept },
        { upsert: true }
      );
      console.log(`  - [${dept._id.toString()}] ${dept.name} (HOD: ${dept.hod})`);
    }

    // 3. Idempotent upsert for students
    console.log("\nSeeding students...");
    for (const student of students) {
      await studentsCol.updateOne(
        { rollNo: student.rollNo },
        { $set: student },
        { upsert: true }
      );
      console.log(`  - [Roll ${student.rollNo}] ${student.name} | Branch: ${student.branch} | Marks: ${student.marks}`);
    }

    const deptCount = await deptCol.countDocuments();
    const studentCount = await studentsCol.countDocuments();

    console.log("\n==================================================");
    console.log("✓ Database seeding complete (idempotent)!");
    console.log(`  Database   : ${DB_NAME}`);
    console.log(`  Departments: ${deptCount} records in "departments"`);
    console.log(`  Students   : ${studentCount} records in "students"`);
    console.log("==================================================");

  } catch (err) {
    console.error("\n[SEED ERROR]", err.message);
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

// Execute seed if run directly
if (require.main === module) {
  seedDatabase();
}

module.exports = { seedDatabase, departments, students, DEPT_IDS };
