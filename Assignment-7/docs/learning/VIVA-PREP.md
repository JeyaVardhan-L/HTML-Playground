# Viva Preparation: 20 High-Yield Questions & Spoken Answers

Use this guide to prepare for your viva voce and practical lab evaluation for Assignment 7.

---

### Q1. What are MongoDB cursor methods and how do they differ from JavaScript array methods?
**Spoken Answer:**  
"Cursor methods like `.sort()` and `.limit()` are applied to a database query *before* documents are retrieved. MongoDB evaluates them inside the database engine in C++, transferring only the final slice of documents across the network. In contrast, JavaScript array methods like `Array.prototype.sort()` require downloading the entire collection into Node.js memory before sorting."

---

### Q2. How do you implement a deterministic tie-breaker in MongoDB's `sort()`?
**Spoken Answer:**  
"By passing multiple fields in the sort specification object. For example, `.sort({ marks: -1, rollNo: 1 })` sorts primarily by marks descending, but if two students have identical marks, it orders them by roll number ascending, ensuring consistent output every time."

---

### Q3. What is the size and structure of a MongoDB `ObjectId`?
**Spoken Answer:**  
"An `ObjectId` is a 12-byte (24-hexadecimal character) unique identifier. It is divided into three parts: a 4-byte timestamp representing the creation second, a 5-byte random value unique to the machine and process, and a 3-byte incrementing counter."

---

### Q4. Why does `collection.findOne({ _id: "65f1..." })` return null even if a document with that ID exists?
**Spoken Answer:**  
"Because MongoDB uses BSON, which enforces strict data types. A plain JavaScript string is BSON type 2, whereas an `ObjectId` is BSON type 7. To find the document, the hex string must be converted to an `ObjectId` instance using `new ObjectId(hexString)`."

---

### Q5. How can you extract the creation date and time from a MongoDB `ObjectId`?
**Spoken Answer:**  
"By calling the `.getTimestamp()` method on any `ObjectId` instance. Because the first 4 bytes encode Unix epoch seconds, MongoDB can derive the exact creation time without needing a separate `createdAt` field."

---

### Q6. What is the difference between `deleteOne()` and `deleteMany()`?
**Spoken Answer:**  
"`deleteOne()` finds and deletes only the first document that matches the filter criteria, even if dozens match. `deleteMany()` deletes all documents in the collection that satisfy the filter criteria and returns a `deletedCount`."

---

### Q7. What query operator is used to find or delete records with values strictly less than a threshold?
**Spoken Answer:**  
"The `$lt` operator (Less Than). For example, `{ marks: { $lt: 40 } }` matches all documents where the numeric `marks` field is strictly below 40."

---

### Q8. Why is it important to include an interactive confirmation step before running destructive deletion scripts?
**Spoken Answer:**  
"Destructive queries like `deleteMany()` permanently remove records. In a production or shared lab environment, an interactive confirmation prompt prevents accidental data loss from typing errors or running the wrong script."

---

### Q9. What does the caret (`^`) symbol mean in a MongoDB regular expression?
**Spoken Answer:**  
"In regular expressions, the caret symbol `^` is an anchor that specifies the match must occur at the very beginning of the string. In `{ name: { $regex: "^M" } }`, it ensures only names starting with the letter 'M' match."

---

### Q10. How do you make a MongoDB `$regex` query case-insensitive?
**Spoken Answer:**  
"Either by passing `$options: "i"` in the query object `{ name: { $regex: "^M", $options: "i" } }`, or by passing a JavaScript RegExp literal with the `i` flag: `{ name: /^m/i }`."

---

### Q11. What is the performance implication of using regular expressions in MongoDB?
**Spoken Answer:**  
"Prefix-anchored regular expressions like `^M` can utilize a B-tree index on the field to quickly find matching entries. However, unanchored regexes (like `.*M.*`) cannot use index ranges and require scanning every document in the collection."

---

### Q12. What is a race condition in a multi-user inventory or library application?
**Spoken Answer:**  
"A race condition occurs when two concurrent requests read the same value (e.g., `copies = 1`), both conclude a copy is available, and both decrement the count, causing the inventory to drop to negative values."

---

### Q13. How does our library management program prevent negative book copies?
**Spoken Answer:**  
"We use an atomic `findOneAndUpdate` operation with the query condition `{ title: titleRegex, copies: { $gt: 0 } }` and update operator `{ $inc: { copies: -1 } }`. If `copies` is zero, the condition fails, no decrement occurs, and no negative numbers are possible."

---

### Q14. What does the `$inc` update operator do in MongoDB?
**Spoken Answer:**  
"`$inc` is an atomic update operator that increments or decrements a numeric field by a specified value. For example, `{ $inc: { copies: 1 } }` increments by one, and `{ $inc: { copies: -1 } }` decrements by one."

---

### Q15. What is the difference between `returnDocument: "before"` and `returnDocument: "after"` in `findOneAndUpdate`?
**Spoken Answer:**  
"By default, `findOneAndUpdate` returns the original document before modifications were applied. Setting `returnDocument: "after"` instructs MongoDB to return the newly updated document containing the updated field values."

---

### Q16. Can `find().sort().limit()` be converted into an aggregation pipeline?
**Spoken Answer:**  
"Yes. An aggregation pipeline using `{ $sort: { marks: -1 } }` followed by `{ $limit: 3 }` achieves the exact same output. However, for simple queries without joins or accumulators, cursor methods are preferred for simplicity and readability."

---

### Q17. What does the `upsert: true` option do in an update operation?
**Spoken Answer:**  
"`upsert` is a portmanteau of 'update' and 'insert'. When `upsert: true` is passed, MongoDB updates the document if it matches the filter, or inserts a brand new document if no matching record is found."

---

### Q18. How can a student recover deleted records after demonstrating Requirement 8 (`delete-below-40`)?
**Spoken Answer:**  
"By running `npm run seed`. Because the seed script is idempotent and uses `updateOne` with `upsert: true`, it re-inserts the missing student records without duplicating any existing records."

---

### Q19. What does `ObjectId.isValid()` do?
**Spoken Answer:**  
"`ObjectId.isValid()` checks whether a given string is a valid 24-character hexadecimal string that can be safely converted into a BSON `ObjectId` without throwing a runtime format exception."

---

### Q20. Why do we avoid using Mongoose in Assignments 6 and 7?
**Spoken Answer:**  
"Because using the native MongoDB Node.js driver teaches the fundamental database protocol, BSON types, cursor mechanics, and aggregation stages without the abstraction layer, virtual getters, and hidden schema behaviors of Mongoose."
