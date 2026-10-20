# Viva Preparation: 20 High-Yield Questions & Spoken Answers

Use this guide to prepare for your viva voce and practical lab evaluation for Assignment 6.

---

### Q1. What is the MongoDB Aggregation Framework?
**Spoken Answer:**  
"The MongoDB aggregation framework is a pipeline-based data processing engine where documents pass through consecutive transformation stages—such as filtering, joining, grouping, and projecting—directly inside the database engine, returning computed results."

---

### Q2. How does `$lookup` work in MongoDB? Which SQL clause is it similar to?
**Spoken Answer:**  
"`$lookup` performs a left outer join between two collections. It takes four parameters: `from` specifies the foreign collection, `localField` is the key in the current collection, `foreignField` is the key in the foreign collection, and `as` is the name of the new array field that holds the joined documents. It is equivalent to a SQL `LEFT OUTER JOIN`."

---

### Q3. Why does `$lookup` always output an array, and why do we often follow it with `$unwind`?
**Spoken Answer:**  
"`$lookup` outputs an array because a left join can match zero, one, or multiple documents. Even for one-to-one relationships, it produces a single-element array. We follow it with `$unwind` to deconstruct that array into a flat sub-document so we can access fields directly."

---

### Q4. What does the `$unwind` stage do?
**Spoken Answer:**  
"`$unwind` deconstructs an array field from the input documents to output one document for each element in the array. For example, if a student has two subjects in an array, `$unwind` duplicates the student fields and emits two separate documents, one per subject."

---

### Q5. What is the purpose of the `$group` stage and what are accumulators?
**Spoken Answer:**  
"`$group` separates documents into groups according to a specified `_id` expression. Accumulators are expressions like `$sum`, `$avg`, `$max`, and `$min` that calculate summary values across all documents that share the same group key."

---

### Q6. What is the difference between `$sum: 1` and `$sum: "$marks"` in a `$group` stage?
**Spoken Answer:**  
"`$sum: 1` increments the accumulator by one for every document in the group, effectively counting the documents. `$sum: "$marks"` adds the numeric value of the `marks` field from each document together to compute a running total."

---

### Q7. Why should `$match` ideally be placed at the beginning of an aggregation pipeline?
**Spoken Answer:**  
"Placing `$match` at the beginning filters out non-qualifying documents early, reducing the working dataset before costly operations like `$lookup`, `$unwind`, or `$group`. It also allows MongoDB to use indexes to accelerate the query."

---

### Q8. What does `$project` do in an aggregation pipeline?
**Spoken Answer:**  
"`$project` reshapes documents by including specific fields with `1`, suppressing `_id` with `0`, renaming fields, and creating computed fields such as rounding averages using `$round`."

---

### Q9. What is the difference between an ordinary cursor query (`find()`) and an aggregation pipeline (`aggregate()`)?
**Spoken Answer:**  
"`find()` simply searches, filters, and returns documents stored in a collection with basic projection and sorting. `aggregate()` performs multi-stage transformations, joins across collections, array flattening, and statistical calculations inside the database."

---

### Q10. What is an `ObjectId` and what are its components?
**Spoken Answer:**  
"An `ObjectId` is a 12-byte (24-hex-character) unique identifier used as the primary key `_id` in MongoDB. It consists of a 4-byte timestamp representing the creation second, a 5-byte random machine and process value, and a 3-byte incrementing counter."

---

### Q11. Why can't we query an `_id` using a plain string like `{ _id: "65f1a1a1..." }`?
**Spoken Answer:**  
"Because MongoDB's BSON specification treats `ObjectId` as a distinct binary type, not a string. To match a document's `_id`, we must wrap the hex string in `new ObjectId(idString)` using the MongoDB driver."

---

### Q12. What is an idempotent database seed script?
**Spoken Answer:**  
"An idempotent seed script produces the exact same database state regardless of how many times it is executed. Instead of calling `insertMany` which would duplicate records on subsequent runs, it uses `updateOne` with `upsert: true` matching on unique keys like `rollNo` or `_id`."

---

### Q13. How does our Express API prevent duplicate student roll numbers?
**Spoken Answer:**  
"At the application layer, `POST /students` checks if `findOne({ rollNo })` returns a document before inserting. At the database layer, we create a unique index on `students(rollNo)` on startup, which rejects collisions with MongoDB error code 11000."

---

### Q14. What HTTP status codes does the Express REST API return and when?
**Spoken Answer:**  
- `200 OK`: Successful retrieval, update, or deletion.  
- `201 Created`: Successful creation of a new student via POST.  
- `400 Bad Request`: Validation failure (missing name/rollNo, negative marks, or duplicate rollNo).  
- `404 Not Found`: Student does not exist for GET, PUT, or DELETE.  
- `500 Internal Server Error`: Unexpected database failure.

---

### Q15. Why do we delete `_id` from the update payload in `PUT /students/:rollNo`?
**Spoken Answer:**  
"In MongoDB, the `_id` field is immutable. If a client mistakenly sends `_id` in the JSON request body, attempting to update `_id` throws a `MongoServerError`. Stripping `_id` before calling `findOneAndUpdate` protects the operation from crashing."

---

### Q16. What is the difference between `PUT` and `POST` in REST?
**Spoken Answer:**  
"`POST` is used to create a new resource and is typically non-idempotent because multiple identical POSTs create multiple records. `PUT` is used to replace or update an existing resource and is idempotent because calling it multiple times produces the same state."

---

### Q17. What is `express.json()` and why is it necessary?
**Spoken Answer:**  
"`express.json()` is a built-in middleware function in Express that reads incoming HTTP request streams containing JSON payloads and parses them into a native JavaScript object attached to `req.body`."

---

### Q18. How do we ensure MongoDB connections are closed when the Express server stops?
**Spoken Answer:**  
"We register signal listeners for `SIGINT` (Ctrl+C) and `SIGTERM`. When triggered, they call `server.close()` to stop accepting new HTTP requests and `client.close()` to cleanly shut down MongoDB connection pool sockets before exiting."

---

### Q19. In Requirement 3, why did we calculate subject averages from the `subjects` array rather than the `marks` field?
**Spoken Answer:**  
"Because the assignment requirement specifically tests `$unwind` on nested subject arrays. The overall `marks` field is a single summary number, whereas the `subjects` array contains distinct individual subject test scores that must be flattened and aggregated."

---

### Q20. Why do we use Port 3002 for Assignment 6?
**Spoken Answer:**  
"Assignment 4 uses port 3000 and Assignment 5 uses port 3001. We use port 3002 to avoid TCP port conflict errors (`EADDRINUSE`) so multiple lab practical servers can run concurrently without interference."
