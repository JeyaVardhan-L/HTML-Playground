# MongoDB from Zero: Core Concepts & Driver Fundamentals

This document provides a thorough, beginner-friendly introduction to MongoDB and how it is used in Node.js applications without third-party abstraction layers like Mongoose.

---

## 1. What is MongoDB?

**MongoDB** is a document-oriented, NoSQL database. Rather than storing records in rigid two-dimensional tables with fixed rows and columns (like MySQL or PostgreSQL), MongoDB stores records as flexible, JSON-like **documents** inside **collections**.

### Comparison: Relational (SQL) vs Document (MongoDB)

| Relational (SQL) Concept | MongoDB Equivalent | Assignment 6 Example |
| :--- | :--- | :--- |
| Database | Database | `waf_assignment_6` |
| Table | Collection | `students`, `departments` |
| Row / Record | Document | `{ rollNo: "101", name: "Aarav", ... }` |
| Column | Field | `branch`, `marks`, `name` |
| Primary Key | `_id` (`ObjectId`) | `_id: ObjectId("65f1b2b2b2b2b2b2b2b2b101")` |
| Foreign Key / JOIN | Reference / `$lookup` | `departmentId` references `departments._id` |
| Grouping / Aggregation | Aggregation Pipeline | `aggregate([ { $group: ... } ])` |

---

## 2. Documents and BSON

On disk and across the network, MongoDB stores documents in **BSON** (Binary JSON). BSON extends JSON by adding support for specialized data types:
- **`ObjectId`**: 12-byte unique identifier used by default for the `_id` field.
- **`Date`**: Millisecond-precision timestamps.
- **`Int32` / `Int64` / `Double`**: Distinct numeric representations.

Example student document in BSON:
```javascript
{
  _id: new ObjectId("65f1b2b2b2b2b2b2b2b2b101"),
  rollNo: "101",
  name: "Aarav Sharma",
  branch: "CSE",
  departmentId: new ObjectId("65f1a1a1a1a1a1a1a1a1a101"),
  marks: 88,
  subjects: [
    { name: "DBMS", marks: 90 },
    { name: "JavaScript", marks: 86 }
  ]
}
```

---

## 3. What is an ObjectId?

Every document stored in MongoDB requires an `_id` field that serves as its unique primary key. When you don't supply an `_id`, MongoDB generates an `ObjectId` automatically.

An `ObjectId` is a 12-byte (24-hex-character) value structured as:
1. **4 bytes**: Unix timestamp of document creation.
2. **5 bytes**: Random machine/process identifier.
3. **3 bytes**: Incrementing counter initialized randomly.

In the native Node.js driver:
```javascript
const { ObjectId } = require("mongodb");

// 1. Generate a new random ObjectId
const id1 = new ObjectId();

// 2. Parse an existing 24-character hexadecimal string
const id2 = new ObjectId("65f1a1a1a1a1a1a1a1a1a101");

// 3. Compare ObjectIds correctly
id1.equals(id2); // true or false
```
> [!IMPORTANT]
> Querying by `_id` requires converting a string to an `ObjectId`:
> `collection.findOne({ _id: new ObjectId(idString) })`
> Passing a plain string `{ _id: idString }` will NOT match an `ObjectId` stored in the database!

---

## 4. Native Driver vs Mongoose

In Assignment 6, we use the **official native MongoDB Node.js driver** (`mongodb`) instead of **Mongoose**:
1. **Clarity**: You see and control the exact operations sent across the wire.
2. **Standard Aggregations**: Aggregation pipelines match the official MongoDB shell syntax 1-to-1.
3. **No Hidden Overhead**: No schema compilation, virtual getters, or unexpected type casting.
4. **Lightweight**: Smaller dependency footprint and faster startup.

---

## 5. Connecting with `MongoClient`

The native driver uses `MongoClient` to manage connection pooling:

```javascript
const { MongoClient } = require("mongodb");

const uri = "mongodb://127.0.0.1:27017/waf_assignment_6";
const client = new MongoClient(uri, { serverSelectionTimeoutMS: 3000 });

async function run() {
  try {
    await client.connect();
    const db = client.db("waf_assignment_6");
    const students = db.collection("students");
    // perform queries...
  } finally {
    await client.close(); // Cleanly release database connections
  }
}
```

---

## 6. Basic CRUD Operations

### 1. `insertOne()`
```javascript
const result = await students.insertOne({
  rollNo: "109",
  name: "Sneha Roy",
  branch: "CSE",
  marks: 85
});
console.log("Inserted ID:", result.insertedId);
```

### 2. `find()` and `findOne()`
```javascript
// Find one document matching criteria
const student = await students.findOne({ rollNo: "101" });

// Find multiple documents and convert cursor to array
const cseStudents = await students.find({ branch: "CSE" }).toArray();
```

### 3. `updateOne()`
```javascript
// Update fields using $set atomic operator
const result = await students.updateOne(
  { rollNo: "101" },
  { $set: { marks: 90, name: "Aarav S." } }
);
console.log("Matched:", result.matchedCount, "Modified:", result.modifiedCount);
```

### 4. `deleteOne()` and `deleteMany()`
```javascript
// Delete a single document by roll number
await students.deleteOne({ rollNo: "109" });

// Delete all documents matching a condition
const result = await students.deleteMany({ marks: { $lt: 40 } });
console.log("Deleted count:", result.deletedCount);
```

---

## 7. Comparison Query Operators

MongoDB provides expressive query operators prefixed with `$`:
- **`$gt`**: Greater than (`{ marks: { $gt: 60 } }`)
- **`$gte`**: Greater than or equal to (`{ marks: { $gte: 60 } }`)
- **`$lt`**: Less than (`{ marks: { $lt: 40 } }`)
- **`$lte`**: Less than or equal to (`{ marks: { $lte: 40 } }`)
- **`$ne`**: Not equal (`{ branch: { $ne: "CSE" } }`)
- **`$in`**: Contained within an array (`{ branch: { $in: ["CSE", "ECE"] } }`)

---

## 8. Unique Indexes and Data Integrity

By default, MongoDB only enforces uniqueness on `_id`. To ensure no two students share the same roll number, we create a **unique index**:

```javascript
await studentsCol.createIndex({ rollNo: 1 }, { unique: true });
```

When an insert or update attempts to use an existing `rollNo`, MongoDB rejects it with error code **11000** (`E11000 duplicate key error collection`), which our Express API catches and translates into a friendly HTTP 400 Bad Request.

---

## 9. Cursor Queries vs Aggregation Pipelines

- **Cursor Queries (`find()`)**: Best for simple lookups, filtering, and sorting of documents as they are stored on disk.
- **Aggregation Pipelines (`aggregate()`)**: A multi-stage processing pipeline where documents flow through consecutive transformation steps (joining, unwinding, grouping, accumulating, and projecting). Calculations run inside the database engine, returning only the computed results to the client.
