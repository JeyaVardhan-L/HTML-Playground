# Web Application Frameworks (WAF) — Lab Assignment 7
## MongoDB Queries, Cursors, Regex, Safe Deletion & Library Management

**Subject:** Web Application Frameworks (WAF) Lab  
**Assignment:** Lab Assignment 7 — MongoDB Queries, Cursor Chaining, Regex & Atomic Updates  
**Technologies:** Node.js, MongoDB Native Driver (`mongodb` v6), JavaScript (ES2022)  
**Database Name:** `waf_assignment_7`  
**Student:** Student Name · Department of Computer Science & Engineering (CSE), 3rd Year  

---

## 1. Assignment Purpose

This lab practical explores essential MongoDB database queries, cursor methods, data typing, and concurrency patterns in **Node.js** using the official native MongoDB Node.js driver (`mongodb`):

1. **Top-K Scoring with Cursors (`sort()` & `limit()`):** Retrieving the top 3 scoring students using native database cursor chaining with deterministic tie-breaking.
2. **BSON Primary Key Resolution (`new ObjectId("...")`):** Working with 12-byte BSON `ObjectId` primary keys and understanding why BSON types do not match plain JavaScript strings.
3. **Safe Destructive Deletion (`deleteMany({ marks: { $lt: 40 } })`):** Removing student records below 40 marks with interactive confirmation safeguards and idempotent data recovery.
4. **Pattern Matching with Regular Expressions (`$regex: "^M"`):** Executing database-side pattern matching with case-insensitive options.
5. **Atomic Inventory Management (Library System):** Implementing a terminal-based book issue/return system utilizing atomic operations (`findOneAndUpdate` with `$inc` and `{ copies: { $gt: 0 } }`) to prevent negative book counts under concurrent access.

---

## 2. Requirement-to-File Mapping

| Requirement | Description | Target File | npm Command |
| :--- | :--- | :--- | :--- |
| **Req 6** | Top three scorers using `sort()` and `limit()` | [`scripts/top-three.js`](file:///c:/Users/user/Downloads/HTML-Playground/HTML-Playground/Assignment-7/scripts/top-three.js) | `npm run top-three` |
| **Req 7** | Find a document by `_id` using `new ObjectId("...")` | [`scripts/find-by-id.js`](file:///c:/Users/user/Downloads/HTML-Playground/HTML-Playground/Assignment-7/scripts/find-by-id.js) | `npm run find-by-id` |
| **Req 8** | Delete all students whose marks are less than 40 | [`scripts/delete-below-40.js`](file:///c:/Users/user/Downloads/HTML-Playground/HTML-Playground/Assignment-7/scripts/delete-below-40.js) | `npm run delete-below-40` |
| **Req 9** | Names starting with M using `$regex` (case-insensitive) | [`scripts/names-starting-m.js`](file:///c:/Users/user/Downloads/HTML-Playground/HTML-Playground/Assignment-7/scripts/names-starting-m.js) | `npm run names-starting-m` |
| **Req 10** | Library management program (atomic issue/return) | [`scripts/library-management.js`](file:///c:/Users/user/Downloads/HTML-Playground/HTML-Playground/Assignment-7/scripts/library-management.js) | `npm run library` |
| **Seed** | Idempotent seeder: departments, students, and books | [`scripts/seed.js`](file:///c:/Users/user/Downloads/HTML-Playground/HTML-Playground/Assignment-7/scripts/seed.js) | `npm run seed` |

---

## 3. Directory Structure

```text
Assignment-7/
├── README.md                      ← Overview, commands, verification checklist & error guide
├── package.json                   ← Declares mongodb driver & npm script shortcuts
├── .gitignore                     ← Ignores node_modules/ and local environment files
├── scripts/
│   ├── seed.js                    ← Idempotent seeder: departments, students & books
│   ├── top-three.js               ← Requirement 6: sort({ marks: -1 }) and limit(3)
│   ├── find-by-id.js              ← Requirement 7: new ObjectId("...") lookup
│   ├── delete-below-40.js         ← Requirement 8: deleteMany({ marks: { $lt: 40 } })
│   ├── names-starting-m.js        ← Requirement 9: $regex "^M" with case-insensitive option
│   └── library-management.js      ← Requirement 10: Interactive and CLI library management
└── docs/
    └── learning/
        ├── START-HERE.md          ← Orientation, architecture diagrams & study plan
        ├── MONGODB-QUERIES.md     ← Cursors, ObjectIds, regex & atomic concurrency
        ├── AGGREGATION-EXPLAINED.md ← Cursors vs aggregation pipelines comparison
        ├── CODE-EXPLANATION.md    ← Line-by-line breakdown of every script
        ├── VIVA-PREP.md           ← 20 high-yield viva questions with spoken model answers
        ├── HANDS-ON-EXERCISES.md  ← 8 beginner hands-on coding exercises
        └── GLOSSARY.md            ← Definitions of key NoSQL and database terms
```

---

## 4. Prerequisites & Free Local MongoDB Setup

Before running this assignment, ensure **Node.js** (v18 or higher) and **npm** are installed.

```powershell
node -v
npm -v
```

### Free Local MongoDB Community Server Setup (Windows)

This assignment connects to a local MongoDB server. MongoDB Community Server is **100% free and open-source**:

#### Option A: Install via Windows Package Manager (winget)
Open an Administrator PowerShell terminal and run:
```powershell
winget install MongoDB.Server
```

#### Option B: Download the Official Installer (MSI)
1. Visit the official MongoDB Community download page:  
   `https://www.mongodb.com/try/download/community`
2. Select **Version: Current**, **Platform: Windows (x64)**, **Package: msi**.
3. Run the installer and choose **"Complete"** installation with **"Install MongoDB as a Service"** checked.
4. Once installed, MongoDB will run as a Windows background service on `localhost:27017`.

#### Verify or Start MongoDB Service
```powershell
# Check if MongoDB service is running
Get-Service -Name MongoDB -ErrorAction SilentlyContinue

# Start the service if stopped
net start MongoDB
```

---

## 5. Installation & Database Seeding (PowerShell)

### Step 1: Navigate to the Assignment 7 Directory
```powershell
cd c:\Users\user\Downloads\HTML-Playground\HTML-Playground\Assignment-7
```

### Step 2: Install Project Dependencies
```powershell
npm install
```

### Step 3: Seed the Database
```powershell
npm run seed
```
*(Runs [`scripts/seed.js`](file:///c:/Users/user/Downloads/HTML-Playground/HTML-Playground/Assignment-7/scripts/seed.js) idempotently, inserting 3 departments, 8 students, and 4 library books)*

---

## 6. How to Run Each Task & Expected Outputs

### Task 1: Top Three Scorers with `sort()` and `limit()` (Requirement 6)
```powershell
npm run top-three
```
**Expected Output:**
```text
================================================================================
Requirement 6: MongoDB Cursor Methods — sort() and limit() (Top 3 Scorers)
================================================================================

Top 3 student scorers retrieved directly via MongoDB cursor:

┌─────────┬────────┬────────────────┬────────┬───────┐
│ (index) │ rollNo │ name           │ branch │ marks │
├─────────┼────────┼────────────────┼────────┼───────┤
│ 0       │ '102'  │ 'Meera Nair'   │ 'CSE'  │ 94    │
│ 1       │ '105'  │ 'Pooja Reddy'  │ 'ECE'  │ 91    │
│ 2       │ '101'  │ 'Aarav Sharma' │ 'CSE'  │ 88    │
└─────────┴────────┴────────────────┴────────┴───────┘

Cursor methods executed on MongoDB server:
1. find({})                     : Scans students collection
2. sort({ marks: -1, rollNo: 1 }): Orders by marks descending with rollNo tie-breaker
3. limit(3)                     : Stops cursor evaluation after 3 qualifying documents
4. project({ ... })             : Transferred only required fields across the network
================================================================================
```

---

### Task 2: Find Document by `_id` using `new ObjectId("...")` (Requirement 7)
```powershell
npm run find-by-id
```
*(Optionally look up a custom ID: `node scripts/find-by-id.js 65f1b2b2b2b2b2b2b2b2b102`)*

**Expected Output:**
```text
================================================================================
Requirement 7: MongoDB Query by Primary Key — new ObjectId("...")
================================================================================

Hexadecimal String : "65f1b2b2b2b2b2b2b2b2b101"
BSON ObjectId Type : ObjectId("65f1b2b2b2b2b2b2b2b2b101")
Timestamp in ID    : 2024-03-14T05:25:21.000Z

--- BSON Type Demonstration ---
1. Querying with plain string: findOne({ _id: "65f1b2b2b2b2b2b2b2b2b101" })
   Result: null ← (null because MongoDB matches on both value AND BSON type)

2. Querying with new ObjectId: findOne({ _id: new ObjectId("65f1b2b2b2b2b2b2b2b2b101") })
   Result: MATCH FOUND!

Retrieved Student Document:
{
  "_id": "65f1b2b2b2b2b2b2b2b2b101",
  "rollNo": "101",
  "name": "Aarav Sharma",
  "branch": "CSE",
  "departmentId": "65f1a1a1a1a1a1a1a1a1a101",
  "marks": 88,
  "subjects": [
    { "name": "DBMS", "marks": 90 },
    { "name": "JavaScript", "marks": 86 }
  ]
}
================================================================================
```

---

### Task 3: Delete Students with Marks < 40 (Requirement 8)
```powershell
npm run delete-below-40
```
*(Interactive mode prompts for confirmation: type `yes` to proceed)*  
*(Non-interactive bypass for automation: `node scripts/delete-below-40.js --confirm`)*

**Expected Output:**
```text
================================================================================
Requirement 8: MongoDB Destructive Delete — deleteMany({ marks: { $lt: 40 } })
================================================================================

-------------------------------- WARNING ---------------------------------------
Target Database    : waf_assignment_7
Target Collection  : students
Filter Condition   : { marks: { $lt: 40 } }
Matching Documents : 2 record(s) found eligible for deletion.
--------------------------------------------------------------------------------

Records that will be PERMANENTLY deleted:
┌─────────┬────────┬────────────────┬────────┬───────┐
│ (index) │ rollNo │ name           │ branch │ marks │
├─────────┼────────┼────────────────┼────────┼───────┤
│ 0       │ '103'  │ 'Rohan Varma'  │ 'CSE'  │ 35    │
│ 1       │ '106'  │ 'Suresh Iyer'  │ 'ECE'  │ 38    │
└─────────┴────────┴────────────────┴────────┴───────┘

Are you SURE you want to delete these records? Type 'yes' to proceed: yes

================================================================================
✓ DELETION COMPLETE: Successfully deleted 2 student record(s).
================================================================================
Remaining students in collection: 6

To RESTORE the deleted sample records at any time, run:
  npm run seed
================================================================================
```

> [!TIP]
> **How to restore deleted sample data:**  
> Simply run `npm run seed`. Because the seed script is idempotent (`updateOne` with `upsert: true`), it immediately restores the deleted records without creating duplicates.

---

### Task 4: Names Starting with 'M' using `$regex` (Requirement 9)
```powershell
npm run names-starting-m
```
**Expected Output:**
```text
================================================================================
Requirement 9: MongoDB Pattern Matching — $regex (Names Starting with 'M')
================================================================================

Query Filter Object: {
  "name": {
    "$regex": "^M",
    "$options": "i"
  }
}
Regex Explanation  : '^' = starts with, 'M' = letter M, 'i' = case-insensitive

Found 2 student(s) matching /^M/i:

┌─────────┬────────┬────────────────┬────────┬───────┐
│ (index) │ rollNo │ name           │ branch │ marks │
├─────────┼────────┼────────────────┼────────┼───────┤
│ 0       │ '104'  │ 'Manish Gupta' │ 'ECE'  │ 78    │
│ 1       │ '102'  │ 'Meera Nair'   │ 'CSE'  │ 94    │
└─────────┴────────┴────────────────┴────────┴───────┘
================================================================================
```

---

### Task 5: Library Management System (Requirement 10)

#### Interactive Terminal Menu
```powershell
npm run library
```
*(Presents options: 1. List all books, 2. Issue a book, 3. Return a book, 4. Exit)*

#### Non-Interactive CLI Commands (Great for quick demonstrations!)
```powershell
# 1. List catalog
node scripts/library-management.js list

# 2. Issue a book
node scripts/library-management.js issue "Clean Code"

# 3. Verify stock decreased
node scripts/library-management.js list

# 4. Attempt to issue out-of-stock book (0 copies)
node scripts/library-management.js issue "JavaScript: The Definitive Guide"
# -> Outputs: ✗ UNAVAILABLE: "JavaScript: The Definitive Guide" is currently out of stock (0 copies available). Cannot issue.

# 5. Return book
node scripts/library-management.js return "Clean Code"
```

**Expected Catalog Output:**
```text
======================== Current Library Catalog ========================
┌─────────┬─────────────────────────────────────┬──────────────────────────┬────────┐
│ (index) │ title                               │ author                   │ copies │
├─────────┼─────────────────────────────────────┼──────────────────────────┼────────┤
│ 0       │ 'Clean Code'                        │ 'Robert C. Martin'       │ 3      │
│ 1       │ 'Database System Concepts'          │ 'Abraham Silberschatz'   │ 4      │
│ 2       │ 'Design Patterns'                   │ 'Erich Gamma et al.'     │ 2      │
│ 3       │ 'JavaScript: The Definitive Guide'  │ 'David Flanagan'         │ 0      │
└─────────┴─────────────────────────────────────┴──────────────────────────┴────────┘
=========================================================================
```

---

## 7. Verification Checklist

- [x] Dependencies install cleanly via `npm install`.
- [x] `npm run seed` idempotently inserts 3 departments, 8 students, and 4 library books.
- [x] `npm run top-three` uses MongoDB cursor chaining (`sort()` and `limit(3)`) with `rollNo` tie-breaker.
- [x] `npm run find-by-id` demonstrates why string matching fails and `new ObjectId("...")` succeeds.
- [x] `npm run delete-below-40` prompts for confirmation and safely deletes only records where `marks < 40`.
- [x] `npm run seed` successfully restores deleted records idempotently.
- [x] `npm run names-starting-m` uses database-level `$regex: "^M"` with `$options: "i"`.
- [x] `npm run library` supports listing, issuing, returning, and out-of-stock rejection.
- [x] Library system uses atomic operations (`findOneAndUpdate` with `{ copies: { $gt: 0 } }` and `$inc: { copies: -1 }`) ensuring copies never drop below zero.

---

## 8. Common Errors & Troubleshooting

### Error: `ECONNREFUSED 127.0.0.1:27017`
- **Cause:** MongoDB service is not started.
- **Solution:** Run `net start MongoDB` in an Administrator PowerShell window or start `mongod.exe`.

### Error: `No students currently have marks below 40`
- **Cause:** `delete-below-40.js` was previously run, deleting the matching records.
- **Solution:** Run `npm run seed` to restore the sample dataset.
