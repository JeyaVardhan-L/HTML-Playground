# Assignment 7 — Start Here: Orientation & Study Guide

Welcome to **Lab Assignment 7** of Web Application Frameworks (WAF). This practical explores advanced MongoDB database operations, cursor chaining, pattern matching, BSON data types, safe destructive deletions, and atomic concurrency patterns in Node.js using the **MongoDB Native Driver** (`mongodb`).

---

## 1. What This Assignment Demonstrates

1. **Top-K Retrieval (`sort()` & `limit()`):** Querying the top 3 scoring students using native cursor chaining with deterministic tie-breaking.
2. **Primary Key Resolution (`new ObjectId("...")`):** Working with 12-byte BSON `ObjectId` values and understanding why BSON types do not match plain strings.
3. **Safe Destructive Deletion (`deleteMany({ marks: { $lt: 40 } })`):** Safely removing underperforming student records with interactive confirmation prompts to prevent accidental data loss.
4. **Pattern Matching with Regular Expressions (`$regex: "^M"`):** Executing case-insensitive name filtering directly inside the database engine.
5. **Atomic Inventory Control (Library Management):** Implementing a terminal-based book issue/return system using atomic operations (`findOneAndUpdate` with `$inc` and `{ copies: { $gt: 0 } }`) that prevent negative inventory under race conditions.

---

## 2. Architecture Diagram

```text
+-----------------------------------------------------------------------------------+
|                                  CLIENT LAYER                                     |
|                                                                                   |
|  - PowerShell CLI commands (npm run top-three, find-by-id, etc.)                  |
|  - Interactive Terminal Interface (npm run library)                               |
+-----------------------------------------------------------------------------------+
                                  |
                                  v Node.js CLI Process
+-----------------------------------------------------------------------------------+
|                            APPLICATION LAYER (Node.js)                            |
|                                                                                   |
|  +-------------------------+  +--------------------------+  +------------------+  |
|  | top-three.js            |  | find-by-id.js            |  | delete-below-40  |  |
|  | - .sort({ marks: -1 })  |  | - new ObjectId(hex)      |  | - deleteMany()   |  |
|  | - .limit(3)             |  | - BSON type comparison   |  | - confirm prompt |  |
|  +-------------------------+  +--------------------------+  +------------------+  |
|  +-------------------------+  +------------------------------------------------+  |
|  | names-starting-m.js     |  | library-management.js                          |  |
|  | - $regex: "^M", "i"     |  | - atomic findOneAndUpdate                      |  |
|  | - database-side regex   |  | - conditional { copies: { $gt: 0 } }           |  |
|  +-------------------------+  +------------------------------------------------+  |
|                               \       |       /                                   |
|                         MongoDB Native Node.js Driver                             |
+-----------------------------------------------------------------------------------+
                                  |
                                  | Wire Protocol (TCP 27017)
                                  v
+-----------------------------------------------------------------------------------+
|                             DATABASE LAYER (MongoDB)                              |
|                          Database: waf_assignment_7                               |
|                                                                                   |
|   +--------------------------+             +----------------------------------+   |
|   |   Collection: students   |             |       Collection: books          |   |
|   |  - _id (ObjectId)        |             |  - _id (ObjectId)                |   |
|   |  - rollNo (unique index) |             |  - title                         |   |
|   |  - name                  |             |  - author                        |   |
|   |  - branch                |             |  - copies (integer >= 0)         |   |
|   |  - marks (0-100)         |             +----------------------------------+   |
|   |  - subjects: [ ... ]     |                                                    |
|   +--------------------------+                                                    |
+-----------------------------------------------------------------------------------+
```

---

## 3. How the Files Relate to One Another

```text
Assignment-7/
├── package.json                   ← Declares mongodb driver & npm script shortcuts
├── .gitignore                     ← Excludes node_modules/ & local .env
├── scripts/
│   ├── seed.js                    ← Idempotent seeder: departments, students & library books
│   ├── top-three.js               ← Requirement 6: sort({ marks: -1 }) and limit(3)
│   ├── find-by-id.js              ← Requirement 7: new ObjectId("...") lookup
│   ├── delete-below-40.js         ← Requirement 8: deleteMany({ marks: { $lt: 40 } }) with prompt
│   ├── names-starting-m.js        ← Requirement 9: $regex "^M" with case-insensitive option
│   └── library-management.js      ← Requirement 10: Interactive & CLI library program
└── docs/
    └── learning/
        ├── START-HERE.md          ← (You are here) Architecture, mental models & study guide
        ├── MONGODB-QUERIES.md     ← Cursors, regex, BSON ObjectId & atomic updates
        ├── AGGREGATION-EXPLAINED.md ← Query pipelines vs cursor methods
        ├── CODE-EXPLANATION.md    ← Line-by-line breakdown of every script
        ├── VIVA-PREP.md           ← 20 high-yield viva questions with model answers
        ├── HANDS-ON-EXERCISES.md  ← 8 beginner hands-on exercises with hints
        └── GLOSSARY.md            ← Definitions of key MongoDB & query terminology
```

---

## 4. Recommended Reading Sequence

1. **`START-HERE.md`** *(This file)*: High-level overview and file connections.
2. **`MONGODB-QUERIES.md`**: Core theory of cursors, ObjectIds, regexes, and atomic updates.
3. **`AGGREGATION-EXPLAINED.md`**: Understand when to use cursor methods vs aggregation pipelines.
4. **`CODE-EXPLANATION.md`**: Detailed line-by-line breakdown of Tasks 6 through 10.
5. **`HANDS-ON-EXERCISES.md`**: 8 small practical experiments to solidify your knowledge.
6. **`VIVA-PREP.md`**: High-yield Q&A covering the exact concepts tested during lab exams.
7. **`GLOSSARY.md`**: Reference dictionary of terms.

---

## 5. 30-Minute Beginner Study Plan

- **Minutes 0–5:** Read `START-HERE.md` and review the architecture diagram.
- **Minutes 5–12:** Read `MONGODB-QUERIES.md` to understand why ObjectIds are binary types and how atomic inventory updates work.
- **Minutes 12–20:** Read `CODE-EXPLANATION.md` for `top-three.js`, `find-by-id.js`, and `library-management.js`.
- **Minutes 20–25:** Try Exercises 1 and 2 in `HANDS-ON-EXERCISES.md`.
- **Minutes 25–30:** Review the viva questions in `VIVA-PREP.md`.
