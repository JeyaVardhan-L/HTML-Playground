# Assignment 6 — Glossary of Terms

Clear, simple definitions for all key NoSQL, MongoDB, Express, and REST terminology used in Assignment 6.

---

### Accumulator
An operator used inside a `$group` stage (such as `$sum`, `$avg`, `$max`, or `$min`) that calculates a single summary value across all documents in a group.

### Aggregation Pipeline
A framework in MongoDB where documents pass through a sequence of stages (like a factory conveyor belt) to be filtered, transformed, grouped, and projected into new shapes.

### BSON (Binary JSON)
A binary-encoded serialization format used by MongoDB to store documents and make remote procedure calls. Extends standard JSON with types like `ObjectId`, `Date`, and specific numeric byte representations.

### Collection
A grouping of MongoDB documents, analogous to a table in a relational database. Collections do not enforce a fixed schema by default.

### CRUD
An acronym for the four basic operations of persistent storage: **C**reate, **R**ead, **U**pdate, and **D**elete.

### Document
A record in MongoDB stored as a JSON-like key-value structure. Analogous to a row in a relational database.

### `$group`
An aggregation stage that separates documents into distinct groups based on a specified group key (`_id`) and applies accumulator expressions to calculate aggregated values.

### Idempotent
An operation that produces the exact same outcome whether it is executed once or multiple times consecutively. For example, `updateOne` with `upsert: true` is idempotent.

### `$lookup`
An aggregation pipeline stage that performs a left outer join between two collections within the same database, attaching matching documents from a foreign collection as an array.

### `$match`
An aggregation pipeline stage that filters documents to pass only those matching specified query conditions to the next pipeline stage. Analogous to the SQL `WHERE` clause.

### MongoClient
The primary class in the official MongoDB Node.js driver used to establish and manage network connection pools with a MongoDB server.

### ObjectId
The default 12-byte (24-hex-character) unique identifier automatically assigned to the `_id` field of every MongoDB document upon creation.

### Port 3002
The TCP port number configured for Assignment 6's Express REST API, selected to prevent conflicts with Assignment 4 (port 3000) and Assignment 5 (port 3001).

### `$project`
An aggregation stage that reshapes each document in the stream, including, suppressing, renaming, or computing new derived fields.

### REST (Representational State Transfer)
An architectural style for network communication that leverages standard HTTP verbs (`GET`, `POST`, `PUT`, `DELETE`) to manipulate resources identified by URIs.

### `$sort`
An aggregation pipeline stage that orders all documents entering the stage by specified sort keys (`1` for ascending, `-1` for descending).

### Unique Index
A database structure that enforces uniqueness on a given field (such as `rollNo`). Prevents duplicate records by rejecting colliding insertions with error code 11000.

### `$unwind`
An aggregation pipeline stage that deconstructs an array field from input documents to output one document for each element in the array.
