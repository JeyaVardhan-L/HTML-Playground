# Assignment 6 — Start Here: Orientation & Study Guide

Welcome to **Lab Assignment 6** of Web Application Frameworks (WAF). This practical explores database-driven web development by connecting **Node.js**, **Express.js**, and the **MongoDB Native Driver** (`mongodb`) to implement advanced aggregation pipelines and a clean RESTful API.

---

## 1. What This Assignment Demonstrates

1. **Relational-Style Joins in NoSQL (`$lookup`):** Joining student records with department details across independent collections without third-party ORMs or Mongoose.
2. **Array Deconstruction (`$unwind`):** Splitting nested subject arrays to perform per-subject arithmetic.
3. **Statistical Aggregations (`$group`):** Grouping records by student or by branch to calculate totals, averages, maximums, and minimums using native accumulators (`$sum`, `$avg`, `$max`, `$min`).
4. **Filtered Aggregation (`$match`):** Combining filtering and grouping to count students scoring above 60 by branch.
5. **Full CRUD REST API:** An Express.js backend on **Port 3002** delivering `POST`, `GET`, `PUT`, and `DELETE` endpoints backed directly by MongoDB.

---

## 2. Architecture & Request Flow

```text
+-----------------------------------------------------------------------------------+
|                                  CLIENT LAYER                                     |
|  - PowerShell Terminal / Invoke-RestMethod                                        |
|  - Node.js CLI Pipeline Scripts (lookup, subject-summary, branch-statistics, etc) |
+-----------------------------------------------------------------------------------+
                                  |
                                  | HTTP (Port 3002) OR Direct MongoDB Driver
                                  v
+-----------------------------------------------------------------------------------+
|                            APPLICATION LAYER (Node.js)                            |
|                                                                                   |
|  +------------------------------+     +----------------------------------------+  |
|  |       Express REST API       |     |        Aggregation CLI Scripts         |  |
|  |       (api/server.js)        |     |               (scripts/*)              |  |
|  |  - JSON body validation      |     |  - lookup-students.js ($lookup/$unwind)|  |
|  |  - Route parameter handling  |     |  - subject-summary.js ($unwind/$group) |  |
|  |  - HTTP Status Codes         |     |  - branch-above-60.js ($match/$group)  |  |
|  |  - Error middleware          |     |  - branch-statistics.js ($avg/$max/min)|  |
|  +------------------------------+     +----------------------------------------+  |
|                                 \     /                                           |
|                     MongoDB Native Node.js Driver                                 |
|                         (MongoClient instance)                                    |
+-----------------------------------------------------------------------------------+
                                  |
                                  | Wire Protocol (TCP 27017)
                                  v
+-----------------------------------------------------------------------------------+
|                             DATABASE LAYER (MongoDB)                              |
|                                Database: waf_lab                                  |
|                                                                                   |
|   +--------------------------+             +----------------------------------+   |
|   |   Collection: students   |             |     Collection: departments      |   |
|   |  - rollNo (unique index) | ----------> |  - _id (ObjectId)                |   |
|   |  - name                  |  References |  - name                          |   |
|   |  - branch                | departmentId|  - hod                           |   |
|   |  - marks                 |             +----------------------------------+   |
|   |  - subjects: [ {..} ]    |                                                    |
|   +--------------------------+                                                    |
+-----------------------------------------------------------------------------------+
```

---

## 3. How the Files Relate to One Another

```text
Assignment-6/
├── package.json                   ← Declares express & mongodb, plus npm run shortcuts
├── .gitignore                     ← Excludes node_modules & local .env
├── api/
│   └── server.js                  ← Requirement 2: Express REST API (Port 3002)
├── scripts/
│   ├── seed.js                    ← Idempotent seeder: 3 departments & 8 students
│   ├── lookup-students.js         ← Requirement 1: $lookup join with departments
│   ├── subject-summary.js         ← Requirement 3: $unwind & $group for subject marks
│   ├── branch-above-60.js         ← Requirement 4: $match & $group for marks > 60
│   └── branch-statistics.js       ← Requirement 5: Branch $avg, $max, $min sorted desc
└── docs/
    └── learning/
        ├── START-HERE.md          ← (You are here) Overview, roadmap & architecture
        ├── MONGODB-FROM-ZERO.md   ← Core NoSQL concepts, driver usage & queries
        ├── EXPRESS-REST-API.md    ← REST architecture, routes, status codes & validation
        ├── AGGREGATION-EXPLAINED.md ← Pipeline stages ($lookup, $unwind, $group, $match)
        ├── CODE-EXPLANATION.md    ← Line-by-line breakdown of every file & query
        ├── VIVA-PREP.md           ← 20 high-yield viva questions with spoken model answers
        ├── HANDS-ON-EXERCISES.md  ← 8 beginner hands-on exercises with hints & solutions
        └── GLOSSARY.md            ← Definitions of key NoSQL and web terminology
```

---

## 4. Recommended Reading Sequence

1. **`START-HERE.md`** *(This file)*: Get your bearings and understand how the parts connect.
2. **`MONGODB-FROM-ZERO.md`**: Understand databases, collections, BSON, and driver basics.
3. **`AGGREGATION-EXPLAINED.md`**: Master pipeline stages (`$lookup`, `$unwind`, `$group`, `$match`).
4. **`EXPRESS-REST-API.md`**: Learn how Express coordinates HTTP requests with database queries.
5. **`CODE-EXPLANATION.md`**: Walk through every line of code across the 6 source files.
6. **`HANDS-ON-EXERCISES.md`**: Practice making small modifications to deepen your intuition.
7. **`VIVA-PREP.md`**: Prepare spoken explanations for your lab examination.
8. **`GLOSSARY.md`**: Quick reference for terms.

---

## 5. 30-Minute Beginner Study Plan

- **Minutes 0–5:** Read this file (`START-HERE.md`) and study the architecture diagram.
- **Minutes 5–12:** Read `AGGREGATION-EXPLAINED.md` to visualize pipeline transformations.
- **Minutes 12–18:** Read `EXPRESS-REST-API.md` to understand the 5 CRUD endpoints and status codes.
- **Minutes 18–24:** Review `CODE-EXPLANATION.md` for `lookup-students.js` and `api/server.js`.
- **Minutes 24–30:** Read the first 10 questions in `VIVA-PREP.md` out loud to practice spoken answers.
