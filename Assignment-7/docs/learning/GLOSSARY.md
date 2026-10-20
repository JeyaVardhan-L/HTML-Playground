# Assignment 7 — Glossary of Terms

Clear, simple definitions for all key MongoDB query, cursor, BSON, regex, and concurrency terminology used in Assignment 7.

---

### Atomic Operation
An operation that completes as a single, indivisible unit of work. In MongoDB, document updates (like `findOneAndUpdate`) are atomic: the condition check and update occur together without the possibility of an intervening write by another process.

### BSON (Binary JSON)
A binary-encoded format used by MongoDB to serialize documents. Enables high-performance traversal and introduces rich data types such as `ObjectId`, `Date`, and specific numeric byte widths.

### Caret (`^`) Anchor
A regular expression metacharacter indicating that the matching pattern must begin at the very start of the string (e.g. `^M` matches `"Meera"` but not `"Aarav"`).

### Cursor
An active pointer to the result set of a query on the MongoDB server. Cursors allow client code to iterate over query results in batches without loading the entire collection into application memory at once.

### `deleteMany()`
A MongoDB collection method that deletes all documents matching a specified query filter and returns the total number of deleted records.

### `findOneAndUpdate()`
A MongoDB method that atomically finds a single document matching query criteria, applies specified update operators (such as `$inc` or `$set`), and returns the document (either before or after update).

### `$inc`
An atomic MongoDB update operator that increments or decrements a numeric field by a specified value.

### `$limit()`
A cursor modifier that constrains the maximum number of documents returned by a query.

### `$lt` (Less Than)
A comparison query operator that matches documents where the value of a specified field is strictly less than a provided number, string, or date.

### `ObjectId`
A 12-byte (24-hex-character) BSON data type automatically assigned as the primary key (`_id`) of MongoDB documents. Contains an encoded 4-byte timestamp, 5-byte process identity, and 3-byte incrementing counter.

### Regular Expression (`$regex`)
A pattern-matching syntax supported by MongoDB for searching string fields using regular expression syntax directly on the database engine.

### `sort()`
A cursor modifier that specifies the order in which matching documents are returned (`1` for ascending, `-1` for descending). Multiple fields can be provided to create deterministic tie-breakers.

### Tie-Breaker
A secondary sort key provided in a `.sort()` clause (e.g. `{ marks: -1, rollNo: 1 }`) to ensure a predictable, deterministic ordering when two or more documents share identical primary sort values.

### `upsert`
A hybrid database operation ("update" + "insert") that updates a document if it matches the filter criteria, or creates a new document if no matching record exists.
