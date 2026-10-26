# MongoDB Aggregation Pipelines Explained: From Concept to Execution

This document explains MongoDB's aggregation framework, breaking down the mechanics of `$lookup`, `$unwind`, `$group`, `$match`, `$project`, and `$sort` as used in Assignment 6.

---

## 1. What is an Aggregation Pipeline?

An **aggregation pipeline** is a multi-stage data processing workflow modeled after the Unix shell pipe (`|`). Documents from a collection enter the first stage, are transformed or filtered, and the output of that stage is passed as input to the next stage.

```text
[ Raw Documents ]
       |
       v
+-------------+
|   Stage 1   |  e.g., $lookup (joins department details)
+-------------+
       | Output of Stage 1
       v
+-------------+
|   Stage 2   |  e.g., $unwind (flattens joined array to object)
+-------------+
       | Output of Stage 2
       v
+-------------+
|   Stage 3   |  e.g., $project (picks fields, shapes response)
+-------------+
       | Output of Stage 3
       v
+-------------+
|   Stage 4   |  e.g., $sort (orders by roll number)
+-------------+
       |
       v
[ Final Computed Result ]
```

All transformations run **inside the MongoDB database engine in C++**, which is far faster and uses significantly less network bandwidth than fetching raw documents into Node.js and processing them with JavaScript array loops.

---

## 2. The Core Pipeline Stages Used in Assignment 6

### Stage 1: `$lookup` — Joining Collections
MongoDB collections are independent, but documents frequently reference each other (e.g., `student.departmentId` references `department._id`).

`$lookup` performs a **left outer join**:
```javascript
{
  $lookup: {
    from: "departments",         // The target collection to join
    localField: "departmentId",  // Field in the incoming (students) documents
    foreignField: "_id",         // Field in the target (departments) collection
    as: "departmentDetails"      // Output array field name
  }
}
```

> [!NOTE]
> `$lookup` always outputs an **array**, even if only one matching document exists.
> To access the joined document as a clean object instead of `departmentDetails[0]`, you follow `$lookup` with `$unwind`.

---

### Stage 2: `$unwind` — Deconstructing Arrays
If a document contains an array, `$unwind` outputs **one document for each element** in that array.

#### Example: Unwinding `departmentDetails` in `lookup-students.js`
Before `$unwind`:
```javascript
{
  name: "Aarav",
  departmentDetails: [
    { name: "Computer Science & Engineering", hod: "Dr. K. S. Rao" }
  ]
}
```
After `$unwind: "$departmentDetails"`:
```javascript
{
  name: "Aarav",
  departmentDetails: {
    name: "Computer Science & Engineering",
    hod: "Dr. K. S. Rao"
  }
}
```

#### Example: Unwinding `subjects` in `subject-summary.js`
Before `$unwind`:
```javascript
{
  rollNo: "101",
  name: "Aarav",
  subjects: [
    { name: "DBMS", marks: 90 },
    { name: "JavaScript", marks: 86 }
  ]
}
```
After `$unwind: "$subjects"`:
Document 1:
```javascript
{ rollNo: "101", name: "Aarav", subjects: { name: "DBMS", marks: 90 } }
```
Document 2:
```javascript
{ rollNo: "101", name: "Aarav", subjects: { name: "JavaScript", marks: 86 } }
```
Now that each subject score is in its own document, `$group` can compute `$sum` and `$avg`!

---

### Stage 3: `$group` & Accumulator Operators
The `$group` stage groups input documents by a specified identifier expression (`_id`) and applies **accumulator expressions** to compute summaries.

#### Accumulators:
- **`$sum: "$field"`**: Computes the numerical sum of values.
- **`$sum: 1`**: Counts the number of documents in the group.
- **`$avg: "$field"`**: Computes the arithmetic mean.
- **`$max: "$field"`**: Identifies the maximum value in the group.
- **`$min: "$field"`**: Identifies the minimum value in the group.

#### Example from `branch-statistics.js`:
```javascript
{
  $group: {
    _id: "$branch",
    averageMarks: { $avg: "$marks" },
    maxMarks: { $max: "$marks" },
    minMarks: { $min: "$marks" },
    totalStudents: { $sum: 1 }
  }
}
```

---

### Stage 4: `$match` — Filtering Documents
`$match` filters documents using standard MongoDB query syntax. It functions like an SQL `WHERE` clause.

#### Best Practice: Place `$match` Early!
In `branch-above-60.js`:
```javascript
{
  $match: {
    marks: { $gt: 60 }
  }
}
```
Placing `$match` as Stage 1 filters out low-scoring students immediately, reducing the number of documents that the subsequent `$group` stage must process.

---

### Stage 5: `$project` — Reshaping the Output
`$project` controls which fields appear in the output, renames fields, and computes new derived values:
- `fieldName: 1` includes the field.
- `_id: 0` suppresses the default `_id` field.
- `newField: "$oldPath.nested"` flattens nested values.
- `averageMarks: { $round: ["$averageMarks", 2] }` rounds a floating-point number to two decimal places.

---

### Stage 6: `$sort` — Ordering Documents
Orders documents by one or more fields:
- `1` = Ascending (A to Z, 0 to 9)
- `-1` = Descending (Z to A, 9 to 0)

In `branch-statistics.js`:
```javascript
{
  $sort: { averageMarks: -1 } // Highest average branch first
}
```

---

## 3. Visual Breakdown of All 4 Pipelines in Assignment 6

### Pipeline 1: `lookup-students.js`
```text
(students collection)
        |
        v Stage 1: $lookup (from: "departments", localField: "departmentId", foreignField: "_id")
        |
        v Stage 2: $unwind: "$departmentDetails"
        |
        v Stage 3: $project (rollNo, name, branch, departmentName, hod)
        |
        v Stage 4: $sort (rollNo: 1)
        |
        v
[ Array of students with full department names and HODs ]
```

### Pipeline 2: `subject-summary.js`
```text
(students collection)
        |
        v Stage 1: $unwind: "$subjects" (splits 8 students into 16 subject rows)
        |
        v Stage 2: $group (_id: { rollNo, name, branch }, total: $sum, avg: $avg, count: $sum: 1)
        |
        v Stage 3: $project (rounds averageSubjectMarks to 2 decimals)
        |
        v Stage 4: $sort (rollNo: 1)
        |
        v
[ Array with rollNo, name, totalSubjectMarks, averageSubjectMarks ]
```

### Pipeline 3: `branch-above-60.js`
```text
(students collection)
        |
        v Stage 1: $match { marks: { $gt: 60 } } (8 students -> 6 qualifying students)
        |
        v Stage 2: $group (_id: "$branch", studentsAbove60Count: { $sum: 1 })
        |
        v Stage 3: $project (branch: "$_id", studentsAbove60Count: 1)
        |
        v Stage 4: $sort (branch: 1)
        |
        v
[ Branch counts: CSE (2), ECE (2), EEE (2) ]
```

### Pipeline 4: `branch-statistics.js`
```text
(students collection)
        |
        v Stage 1: $group (_id: "$branch", avg: $avg, max: $max, min: $min, total: $sum: 1)
        |
        v Stage 2: $project (branch, avg rounded to 2 decimals, max, min, total)
        |
        v Stage 3: $sort { averageMarks: -1 } (descending)
        |
        v
[ CSE (avg: 72.33), ECE (avg: 69.00), EEE (avg: 68.50) ]
```
