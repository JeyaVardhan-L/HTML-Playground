# Aggregation Pipelines vs Cursor Queries: When to Use Which

In Assignment 6, we used the **Aggregation Framework** (`aggregate()`) with stages like `$lookup`, `$unwind`, and `$group`. In Assignment 7, we primarily use **Cursor Queries** (`find().sort().limit()`).

This document clarifies the architectural differences between cursor queries and aggregation pipelines, explaining when to use each approach.

---

## 1. Overview Comparison

| Characteristic | Cursor Queries (`find()`) | Aggregation Pipelines (`aggregate()`) |
| :--- | :--- | :--- |
| **Primary Goal** | Retrieve stored documents with basic filtering, projection, and sorting. | Compute new derived data, join collections, flatten arrays, and calculate statistics. |
| **Methods / Syntax** | Method chaining: `.find().sort().limit()` | Array of stage objects: `aggregate([ { $match }, { $group } ])` |
| **Complexity** | Simple, lightweight, and easy to read. | Powerful, multi-stage, and functional pipeline. |
| **Cross-Collection Joins** | Not supported (single collection only). | Supported via `$lookup`. |
| **Grouping & Accumulators** | Not supported. | Supported via `$group` (`$sum`, `$avg`, etc.). |
| **Array Transformations** | Cannot deconstruct arrays. | Deconstructs arrays via `$unwind`. |
| **Index Utilization** | Highly optimized for single-key and compound indexes. | Indexes used in early stages (`$match`, early `$sort`). |

---

## 2. Converting Assignment 7 Cursor Queries to Aggregation Pipelines

Any query in Assignment 7 *can* be expressed as an aggregation pipeline, but cursor methods are cleaner when complex transformations are not needed.

### Example 1: `top-three.js`

#### Cursor Approach (Assignment 7 Implementation):
```javascript
const results = await studentsCol
  .find({})
  .sort({ marks: -1, rollNo: 1 })
  .limit(3)
  .toArray();
```

#### Equivalent Aggregation Pipeline:
```javascript
const results = await studentsCol.aggregate([
  { $sort: { marks: -1, rollNo: 1 } },
  { $limit: 3 }
]).toArray();
```
*Why cursor is better here:* Simpler syntax and lower driver overhead.

---

### Example 2: `names-starting-m.js`

#### Cursor Approach (Assignment 7 Implementation):
```javascript
const results = await studentsCol
  .find({ name: { $regex: "^M", $options: "i" } })
  .toArray();
```

#### Equivalent Aggregation Pipeline:
```javascript
const results = await studentsCol.aggregate([
  { $match: { name: { $regex: "^M", $options: "i" } } }
]).toArray();
```
*Why cursor is better here:* Standard query filters do not require the overhead of a pipeline wrapper.

---

## 3. Decision Matrix: Which Tool Should You Choose?

```text
Do you need to join collections ($lookup)?
  ├── YES ──> Use Aggregation Pipeline (aggregate)
  └── NO
       │
       Does the operation calculate averages, sums, or groupings ($group)?
         ├── YES ──> Use Aggregation Pipeline (aggregate)
         └── NO
              │
              Do you need to deconstruct arrays ($unwind)?
                ├── YES ──> Use Aggregation Pipeline (aggregate)
                └── NO
                     │
                     Are you just filtering, sorting, or limiting documents?
                       └── YES ──> Use Cursor Methods (find().sort().limit())
```

By mastering both cursor queries (Assignment 7) and aggregation pipelines (Assignment 6), you have the full spectrum of MongoDB data retrieval tools at your command.
