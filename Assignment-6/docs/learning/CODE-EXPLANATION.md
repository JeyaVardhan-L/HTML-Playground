# Code Explanation: Complete Line-by-Line Breakdown for Assignment 6

This document breaks down every script and route in Assignment 6 into small, understandable blocks. Use this guide during lab preparation to understand what each line does and why it is written this way.

---

## 1. `scripts/seed.js` — Idempotent Database Seeder

### What it Does
Connects to MongoDB, ensures a unique index on student roll numbers, and inserts or updates 3 departments and 8 students using idempotent `updateOne` with `upsert: true`.

### Code Walkthrough

#### Block 1: Imports and Configuration
```javascript
const { MongoClient, ObjectId } = require("mongodb");

const MONGODB_URI = process.env.MONGODB_URI || "mongodb://127.0.0.1:27017/waf_assignment_6";
const DB_NAME = "waf_assignment_6";
```
- `MongoClient`: The official driver class that creates database connections.
- `ObjectId`: Class to generate or parse 12-byte BSON identifiers.
- `MONGODB_URI`: Uses an environment variable if provided, or defaults to local port 27017.

#### Block 2: Stable Department ObjectIds & Data Definitions
```javascript
const DEPT_IDS = {
  CSE: new ObjectId("65f1a1a1a1a1a1a1a1a1a101"),
  ECE: new ObjectId("65f1a1a1a1a1a1a1a1a1a102"),
  EEE: new ObjectId("65f1a1a1a1a1a1a1a1a1a103")
};
```
- Hardcoding stable ObjectIds guarantees that subsequent scripts and tests reference identical, predictable keys across every run and machine.

#### Block 3: Unique Index Creation & Idempotent Upserts
```javascript
await studentsCol.createIndex({ rollNo: 1 }, { unique: true });

for (const student of students) {
  await studentsCol.updateOne(
    { rollNo: student.rollNo },
    { $set: student },
    { upsert: true }
  );
}
```
- `createIndex({ rollNo: 1 }, { unique: true })`: Prevents any two documents from having the same `rollNo`.
- `updateOne(filter, update, { upsert: true })`: If a document matching `rollNo` exists, `$set` updates its fields. If not, MongoDB inserts a new document. Running this script 100 times never creates duplicates!

---

## 2. `scripts/lookup-students.js` — Requirement 1: `$lookup` Join

### What it Does
Performs a real left outer join between the `students` collection and the `departments` collection using `$lookup` and `$unwind`.

### Pipeline Walkthrough

#### Stage 1: `$lookup`
```javascript
{
  $lookup: {
    from: "departments",
    localField: "departmentId",
    foreignField: "_id",
    as: "departmentDetails"
  }
}
```
- `from`: The target collection name (`departments`).
- `localField`: The reference field in the student document (`departmentId`).
- `foreignField`: The matching primary key in the department document (`_id`).
- `as`: The name of the new field where matched documents are stored as an array.

#### Stage 2: `$unwind`
```javascript
{
  $unwind: {
    path: "$departmentDetails",
    preserveNullAndEmptyArrays: false
  }
}
```
- Flattens `$departmentDetails` from `[ { name: "...", hod: "..." } ]` into a plain object `{ name: "...", hod: "..." }`.

#### Stage 3 & 4: `$project` and `$sort`
```javascript
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
{ $sort: { rollNo: 1 } }
```
- Strips internal IDs, flattens `departmentDetails.name` to `departmentName`, and sorts ascending by `rollNo`.

### Expected Output
```text
┌─────────┬────────┬────────────────┬────────┬──────────────────────────────────────────┬─────────────────┐
│ (index) │ rollNo │ name           │ branch │ departmentName                           │ hod             │
├─────────┼────────┼────────────────┼────────┼──────────────────────────────────────────┼─────────────────┤
│ 0       │ '101'  │ 'Aarav Sharma' │ 'CSE'  │ 'Computer Science & Engineering'         │ 'Dr. K. S. Rao' │
│ 1       │ '102'  │ 'Meera Nair'   │ 'CSE'  │ 'Computer Science & Engineering'         │ 'Dr. K. S. Rao' │
│ ...     │ ...    │ ...            │ ...    │ ...                                      │ ...             │
└─────────┴────────┴────────────────┴────────┴──────────────────────────────────────────┴─────────────────┘
```

### Try It Yourself
Try removing Stage 2 (`$unwind`) and inspect the output. You will notice `departmentDetails` displays as an array `[Object]` instead of flattened fields.

---

## 3. `api/server.js` — Requirement 2: Express REST API

### What it Does
Provides a full CRUD REST API on port 3002 using Express and the native MongoDB driver.

### Route Breakdown

#### Block 1: `POST /students`
```javascript
app.post("/students", async (req, res) => {
  const { rollNo, name, branch, departmentId, marks, subjects } = req.body;

  if (!rollNo || typeof rollNo !== "string" || rollNo.trim() === "") {
    return res.status(400).json({ error: "Validation failed: 'rollNo' is required and must be a non-empty string." });
  }
  // validate name, marks, departmentId...
  const existing = await studentsCol.findOne({ rollNo: rollNo.trim() });
  if (existing) {
    return res.status(400).json({ error: `Duplicate key: A student with roll number '${rollNo}' already exists.` });
  }

  const result = await studentsCol.insertOne(newStudent);
  return res.status(201).json({ message: "Student created successfully", student: { _id: result.insertedId, ...newStudent } });
});
```
- Validates data types before touching the database.
- Checks for duplicates and returns standard HTTP `400 Bad Request`.
- On success, returns `201 Created` with the newly assigned `_id`.

#### Block 2: `GET /students` and `GET /students/:rollNo`
```javascript
app.get("/students", async (req, res) => {
  const students = await studentsCol.find({}).sort({ rollNo: 1 }).toArray();
  res.status(200).json(students);
});

app.get("/students/:rollNo", async (req, res) => {
  const student = await studentsCol.findOne({ rollNo: req.params.rollNo.trim() });
  if (!student) return res.status(404).json({ error: "Student not found." });
  res.status(200).json(student);
});
```
- `find({}).toArray()` fetches all documents as a JavaScript array.
- `findOne({ rollNo })` searches by the unique business key. If null, returns `404 Not Found`.

#### Block 3: `PUT /students/:rollNo`
```javascript
app.put("/students/:rollNo", async (req, res) => {
  const updates = { ...req.body };
  delete updates._id; // Safety: Never permit changing MongoDB's immutable _id

  const result = await studentsCol.findOneAndUpdate(
    { rollNo: req.params.rollNo.trim() },
    { $set: updates },
    { returnDocument: "after" }
  );

  if (!result) return res.status(404).json({ error: "Student not found." });
  res.status(200).json({ message: "Updated successfully", student: result });
});
```
- `delete updates._id`: Prevents `MongoServerError: Performing an update on the path '_id' would modify the immutable field '_id'`.
- `{ returnDocument: "after" }`: Ensures the response contains the updated document, not the stale pre-update document.

#### Block 4: `DELETE /students/:rollNo`
```javascript
app.delete("/students/:rollNo", async (req, res) => {
  const result = await studentsCol.deleteOne({ rollNo: req.params.rollNo.trim() });
  if (result.deletedCount === 0) return res.status(404).json({ error: "Student not found." });
  res.status(200).json({ message: "Student deleted successfully", deletedRollNo: req.params.rollNo });
});
```
- Verifies `deletedCount === 0` to return `404` when the user tries to delete a non-existent student.

---

## 4. `scripts/subject-summary.js` — Requirement 3: `$unwind` & `$group`

### What it Does
Calculates total subject marks and average subject marks per student by deconstructing the nested `subjects` array.

### Pipeline Breakdown
```javascript
const pipeline = [
  // 1. Deconstruct array into individual subject records
  { $unwind: "$subjects" },
  // 2. Group by student rollNo, name, and branch
  {
    $group: {
      _id: { rollNo: "$rollNo", name: "$name", branch: "$branch" },
      totalSubjectMarks: { $sum: "$subjects.marks" },
      averageSubjectMarks: { $avg: "$subjects.marks" },
      subjectCount: { $sum: 1 }
    }
  },
  // 3. Project fields and round average
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
  { $sort: { rollNo: 1 } }
];
```
- **Why `$unwind` is needed:** MongoDB cannot calculate an `$avg` directly across nested array objects inside a single document without unwinding them into top-level values for the accumulator.

---

## 5. `scripts/branch-above-60.js` — Requirement 4: `$match` & `$group`

### What it Does
Filters students whose overall `marks` are greater than 60 and counts how many qualifying students exist in each branch.

### Pipeline Breakdown
```javascript
const pipeline = [
  // 1. Filter documents first
  { $match: { marks: { $gt: 60 } } },
  // 2. Group by branch and count
  {
    $group: {
      _id: "$branch",
      studentsAbove60Count: { $sum: 1 }
    }
  },
  // 3. Reshape output
  {
    $project: {
      _id: 0,
      branch: "$_id",
      studentsAbove60Count: 1
    }
  },
  { $sort: { branch: 1 } }
];
```
- **Why `$match` comes first:** Placing `$match` as Stage 1 discards documents with `marks <= 60` before the grouping operation, improving query speed and memory efficiency.

---

## 6. `scripts/branch-statistics.js` — Requirement 5: Statistical Accumulators

### What it Does
Calculates branch-wise average marks (`$avg`), maximum marks (`$max`), and minimum marks (`$min`), sorted in descending order of average marks.

### Pipeline Breakdown
```javascript
const pipeline = [
  {
    $group: {
      _id: "$branch",
      averageMarks: { $avg: "$marks" },
      maxMarks: { $max: "$marks" },
      minMarks: { $min: "$marks" },
      totalStudents: { $sum: 1 }
    }
  },
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
  { $sort: { averageMarks: -1 } } // Highest branch average first
];
```
- `averageMarks: -1`: Sorts descending so the faculty can immediately see the top-performing branch.
