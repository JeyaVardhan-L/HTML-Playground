# Code Explanation: Complete Line-by-Line Breakdown for Assignment 7

This document walks through every script in Assignment 7, explaining the design decisions, query operators, variables, and logic flow in small, readable blocks.

---

## 1. `scripts/top-three.js` — Requirement 6: Top 3 Scorers with `sort()` and `limit()`

### What it Does
Queries the `students` collection, sorts students by overall `marks` in descending order with a deterministic tie-breaker on `rollNo`, restricts the cursor to 3 documents, and displays the results in a formatted table.

### Code Walkthrough
```javascript
const topStudents = await studentsCol
  .find({})
  .project({ _id: 0, rollNo: 1, name: 1, branch: 1, marks: 1 })
  .sort({ marks: -1, rollNo: 1 })
  .limit(3)
  .toArray();
```

#### Block Breakdown:
- `find({})`: Initiates a query against all documents in `students`.
- `project({ _id: 0, rollNo: 1, ... })`: Projection applied at the cursor level. Transmits only the required fields over the network, omitting the 12-byte `_id` and nested subject arrays.
- `sort({ marks: -1, rollNo: 1 })`:
  - `marks: -1`: Primary sort key descending (highest marks first).
  - `rollNo: 1`: Secondary sort key ascending (deterministic tie-breaker if two students have identical marks).
- `limit(3)`: Informs the MongoDB query planner to halt cursor execution immediately after finding 3 matching records.
- `toArray()`: Exhausts the cursor and returns an array of documents.

### Expected Output
```text
┌─────────┬────────┬────────────────┬────────┬───────┐
│ (index) │ rollNo │ name           │ branch │ marks │
├─────────┼────────┼────────────────┼────────┼───────┤
│ 0       │ '102'  │ 'Meera Nair'   │ 'CSE'  │ 94    │
│ 1       │ '105'  │ 'Pooja Reddy'  │ 'ECE'  │ 91    │
│ 2       │ '101'  │ 'Aarav Sharma' │ 'CSE'  │ 88    │
└─────────┴────────┴────────────────┴────────┴───────┘
```

### Try It Yourself
Change `.limit(3)` to `.limit(5)` to display the top five scorers instead of three.

---

## 2. `scripts/find-by-id.js` — Requirement 7: Primary Key Resolution with `new ObjectId("...")`

### What it Does
Demonstrates looking up a document by its primary key `_id` using the BSON `ObjectId` class, highlighting why plain string lookups fail.

### Code Walkthrough

#### Block 1: Validating and Instantiating ObjectId
```javascript
const { MongoClient, ObjectId } = require("mongodb");

const idHex = "65f1b2b2b2b2b2b2b2b2b101";

if (!ObjectId.isValid(idHex)) {
  console.error("Invalid hex format");
  return;
}

const objectId = new ObjectId(idHex);
```
- `ObjectId.isValid(idHex)`: Verifies that the string is exactly 24 hexadecimal characters (0-9, a-f) before attempting instantiation.
- `new ObjectId(idHex)`: Creates the 12-byte BSON representation.

#### Block 2: The String vs BSON Contrast
```javascript
// Query 1: Plain string query
const stringResult = await studentsCol.findOne({ _id: idHex });
// Returns: null

// Query 2: BSON ObjectId query
const properResult = await studentsCol.findOne({ _id: objectId });
// Returns: Full Aarav Sharma student document
```
- **Why this happens:** In MongoDB, BSON data types are strictly enforced. An `_id` field stored as an `ObjectId` (Type 7) will never match a query searching for a `String` (Type 2), even if the characters match.

### Expected Output
```text
Hexadecimal String : "65f1b2b2b2b2b2b2b2b2b101"
BSON ObjectId Type : ObjectId("65f1b2b2b2b2b2b2b2b2b101")
Timestamp in ID    : 2024-03-14T05:25:21.000Z

--- BSON Type Demonstration ---
1. Querying with plain string: findOne({ _id: "65f1b2b2b2b2b2b2b2b2b101" })
   Result: null ← (null because MongoDB matches on both value AND BSON type)

2. Querying with new ObjectId: findOne({ _id: new ObjectId("65f1b2b2b2b2b2b2b2b2b101") })
   Result: MATCH FOUND!
```

---

## 3. `scripts/delete-below-40.js` — Requirement 8: Safe Deletion with `deleteMany()`

### What it Does
Deletes all students whose overall score is less than 40 (`marks < 40`) while protecting against accidental data loss with an interactive confirmation prompt.

### Code Walkthrough

#### Block 1: Identifying Candidates Before Deletion
```javascript
const filter = { marks: { $lt: 40 } };
const candidates = await studentsCol.find(filter).toArray();
```
- Always preview records matching a destructive filter before executing the delete command.

#### Block 2: Interactive Prompt & CLI Flag
```javascript
const args = process.argv.slice(2);
const autoConfirmed = args.some(arg => ["--confirm", "--yes", "-y"].includes(arg.toLowerCase()));

if (!autoConfirmed) {
  const response = await askConfirmation("Are you SURE? Type 'yes': ");
  if (response !== "yes") return;
}
```
- Interactive runs prompt the user.
- Automated testing can pass `--confirm` or `-y` without hanging on `stdin`.

#### Block 3: Executing `deleteMany()`
```javascript
const deleteResult = await studentsCol.deleteMany(filter);
console.log("Deleted count:", deleteResult.deletedCount);
```
- Deletes all qualifying documents in one call.
- Qualifying students in our dataset: Rohan Varma (marks 35) and Suresh Iyer (marks 38) → 2 deleted records.

---

## 4. `scripts/names-starting-m.js` — Requirement 9: `$regex` Pattern Matching

### What it Does
Uses MongoDB's `$regex` operator with the case-insensitive flag (`$options: "i"`) to find all students whose names begin with the letter M.

### Code Walkthrough
```javascript
const query = {
  name: {
    $regex: "^M",
    $options: "i"
  }
};

const matchingStudents = await studentsCol
  .find(query)
  .project({ _id: 0, rollNo: 1, name: 1, branch: 1, marks: 1 })
  .sort({ name: 1 })
  .toArray();
```

#### Why `^M` Works:
- `^`: Regular expression anchor meaning "start of string".
- `M`: The literal character M.
- `$options: "i"`: Case-insensitive modifier.
- **Results matched:**
  - `Meera Nair` (Starts with M)
  - `Manish Gupta` (Starts with M)

---

## 5. `scripts/library-management.js` — Requirement 10: Atomic Library Operations

### What it Does
Provides a terminal-based book management system (list, issue, return) utilizing atomic update operators so that book copies never drop below zero.

### Code Walkthrough

#### Block 1: Atomic Issue (`findOneAndUpdate` with `$inc: -1`)
```javascript
const result = await booksCol.findOneAndUpdate(
  {
    title: new RegExp(`^${title.trim()}$`, "i"),
    copies: { $gt: 0 } // Condition: At least one copy must be present!
  },
  {
    $inc: { copies: -1 } // Atomic decrement
  },
  {
    returnDocument: "after"
  }
);
```
- **Atomicity:** The condition check (`copies > 0`) and modification (`$inc: -1`) happen in a single, atomic operation inside the database engine.
- If a book has 0 copies, the query fails to find a matching document, returning `null` without modifying the record.
- **Result:** Copies can **never** become negative, even under heavy concurrency!

#### Block 2: Atomic Return (`findOneAndUpdate` with `$inc: +1`)
```javascript
const result = await booksCol.findOneAndUpdate(
  { title: new RegExp(`^${title.trim()}$`, "i") },
  { $inc: { copies: 1 } },
  { returnDocument: "after" }
);
```
- Increments `copies` atomically upon book return.

#### Block 3: Dual Operating Modes
- **Interactive Menu:** Prompts with options 1–4 when run without arguments (`node scripts/library-management.js`).
- **CLI Commands:** Directly executes subcommands for scripting:
  - `node scripts/library-management.js list`
  - `node scripts/library-management.js issue "Clean Code"`
  - `node scripts/library-management.js return "Clean Code"`
