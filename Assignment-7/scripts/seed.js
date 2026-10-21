/**
 * Assignment 7: Seed Script for MongoDB Database (waf_assignment_7)
 *
 * Idempotently seeds:
 * 1. "departments" collection with 3 distinct departments (CSE, ECE, EEE)
 * 2. "students" collection with 8 realistic student records
 * 3. "books" collection with 4 library book records (including 0-copy edge case)
 *
 * Characteristics:
 * - Stable ObjectIds for deterministic testing (e.g. find-by-id)
 * - Safe upsert operations (updateOne with upsert: true)
 * - Can be run repeatedly after destructive tests (e.g. delete-below-40) to restore data
 */

const { MongoClient, ObjectId } = require("mongodb");

const MONGODB_URI = process.env.MONGODB_URI || "mongodb://127.0.0.1:27017/waf_assignment_7";
const DB_NAME = "waf_assignment_7";

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

// Stable Student ObjectIds (Roll 101: 65f1b2b2b2b2b2b2b2b2b101 is used by find-by-id.js)
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

// Sample Books for Requirement 10 (Library Management)
const books = [
  {
    _id: new ObjectId("65f1c3c3c3c3c3c3c3c3c101"),
    title: "Clean Code",
    author: "Robert C. Martin",
    copies: 3
  },
  {
    _id: new ObjectId("65f1c3c3c3c3c3c3c3c3c102"),
    title: "Design Patterns",
    author: "Erich Gamma et al.",
    copies: 2
  },
  {
    _id: new ObjectId("65f1c3c3c3c3c3c3c3c3c103"),
    title: "JavaScript: The Definitive Guide",
    author: "David Flanagan",
    copies: 0 // Demonstrates zero-copy availability check
  },
  {
    _id: new ObjectId("65f1c3c3c3c3c3c3c3c3c104"),
    title: "Database System Concepts",
    author: "Abraham Silberschatz",
    copies: 4
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
    const booksCol = db.collection("books");

    // 1. Ensure unique indexes
    await studentsCol.createIndex({ rollNo: 1 }, { unique: true });
    await booksCol.createIndex({ title: 1 }, { unique: true });
    console.log("✓ Created/verified unique indexes on students(rollNo) and books(title).");

    // 2. Upsert departments
    console.log("\nSeeding departments...");
    for (const dept of departments) {
      await deptCol.updateOne(
        { _id: dept._id },
        { $set: dept },
        { upsert: true }
      );
      console.log(`  - [${dept._id.toString()}] ${dept.name} (HOD: ${dept.hod})`);
    }

    // 3. Upsert students
    console.log("\nSeeding students...");
    for (const student of students) {
      await studentsCol.updateOne(
        { rollNo: student.rollNo },
        { $set: student },
        { upsert: true }
      );
      console.log(`  - [Roll ${student.rollNo}] ${student.name} | Branch: ${student.branch} | Marks: ${student.marks}`);
    }

    // 4. Upsert library books
    console.log("\nSeeding library books...");
    for (const book of books) {
      await booksCol.updateOne(
        { title: book.title },
        { $set: book },
        { upsert: true }
      );
      console.log(`  - "${book.title}" by ${book.author} (Copies available: ${book.copies})`);
    }

    const deptCount = await deptCol.countDocuments();
    const studentCount = await studentsCol.countDocuments();
    const bookCount = await booksCol.countDocuments();

    console.log("\n==================================================");
    console.log("✓ Database seeding complete (idempotent)!");
    console.log(`  Database   : ${DB_NAME}`);
    console.log(`  Departments: ${deptCount} records in "departments"`);
    console.log(`  Students   : ${studentCount} records in "students"`);
    console.log(`  Books      : ${bookCount} records in "books"`);
    console.log("==================================================");

  } catch (err) {
    console.error("\n[SEED ERROR]", err.message);
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
  seedDatabase();
}

module.exports = { seedDatabase, departments, students, books, DEPT_IDS };
