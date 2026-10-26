# MongoDB Query Mechanics: Cursors, ObjectIds, Regex & Atomic Updates

This document covers the database theory and mechanics behind the queries implemented in Assignment 7.

---

## 1. What is a MongoDB Cursor?

When you call `collection.find()`, MongoDB does not immediately load all matching documents into Node.js memory. Instead, it returns a **cursor**—a pointer to the result set on the database server.

```javascript
// Returns a cursor, does NOT load all documents into memory yet
const cursor = studentsCol.find({});

// Chain modifiers to the cursor
cursor.sort({ marks: -1, rollNo: 1 }).limit(3);

// Execute the query on the database and retrieve documents as an array
const results = await cursor.toArray();
```

### Why Cursor Modifiers are Superior to In-Memory Processing

| Approach | Where Execution Happens | Memory Usage | Network Overhead |
| :--- | :--- | :--- | :--- |
| **Cursor Chaining (`.sort().limit(3)`)** | Inside MongoDB engine in C++ | Minimal (stops after 3 matches) | Sends only 3 documents |
| **In-Memory (`array.sort().slice(0, 3)`)** | Inside Node.js V8 runtime | High (fetches entire collection) | Sends all documents |

If a collection contains 1,000,000 students, `find().sort().limit(3)` reads an index and sends exactly 3 documents across the network. An in-memory JavaScript sort would transfer all 1,000,000 documents across the network into Node.js memory, causing severe latency and potential out-of-memory crashes!

---

## 2. BSON `ObjectId` Demystified

Every document created in MongoDB receives an `_id` field of type `ObjectId` unless explicitly overridden.

### Anatomy of an ObjectId (12 Bytes / 24 Hex Characters)
```text
  65f1b2b2   b2b2b2b2b2   b101
 | 4 Bytes |   5 Bytes   | 3 Bytes |
  Timestamp   Machine/PID   Counter
```
1. **Timestamp (4 bytes):** Unix epoch seconds. You can extract the exact creation time with `objectId.getTimestamp()`.
2. **Process/Random Value (5 bytes):** Uniquely identifies the machine and process that generated the ID.
3. **Incrementing Counter (3 bytes):** Sequence number initialized to a random value.

### Why `{ _id: "hexString" }` Fails
In `scripts/find-by-id.js`:
```javascript
const hexString = "65f1b2b2b2b2b2b2b2b2b101";

// 1. Plain String Query -> FAILS (returns null)
await studentsCol.findOne({ _id: hexString });

// 2. ObjectId Query -> SUCCEEDS (returns document)
await studentsCol.findOne({ _id: new ObjectId(hexString) });
```

MongoDB uses **BSON** (Binary JSON). In BSON:
- String has type code **`2`**.
- ObjectId has type code **`7`**.

MongoDB matches documents on both **field name**, **value**, and **BSON type**. A string value `"65f1..."` will never match an `ObjectId("65f1...")` value, even though their printed representations look identical!

---

## 3. Destructive Operations: `deleteMany()` & Safe Practices

MongoDB provides two deletion methods:
- **`deleteOne(filter)`**: Deletes the first document matching the filter.
- **`deleteMany(filter)`**: Deletes all documents matching the filter.

In `scripts/delete-below-40.js`:
```javascript
const filter = { marks: { $lt: 40 } };
const result = await studentsCol.deleteMany(filter);
console.log("Deleted count:", result.deletedCount);
```

### Safety Rules for Destructive Operations
1. **Always Preview Before Deleting:** Query matching records with `find(filter)` and display them before deleting.
2. **Require Confirmation:** In interactive environments, ask the operator to type `"yes"` before executing `deleteMany()`.
3. **Provide Non-Interactive Flags:** Allow automated CI/CD or test scripts to bypass prompts safely using explicit flags (e.g. `--confirm` or `-y`).
4. **Idempotent Recovery:** Always provide an idempotent seed script (`npm run seed`) so accidentally deleted records can be restored instantly.

---

## 4. Regular Expressions with `$regex`

MongoDB supports Perl-Compatible Regular Expressions (PCRE) using the `$regex` operator.

In `scripts/names-starting-m.js`:
```javascript
const query = {
  name: {
    $regex: "^M",
    $options: "i"
  }
};
const matches = await studentsCol.find(query).toArray();
```

### Breakdown of the Expression:
- **`^` (Caret Anchor):** Specifies that the pattern must match starting at the very beginning of the string.
  - `"Meera Nair"` matches because `"M"` is at index 0.
  - `"Raman Mathur"` does NOT match because `"M"` is in the second word.
- **`M`:** The character to match.
- **`$options: "i"`:** Case-insensitive flag. Matches both uppercase `"M"` and lowercase `"m"`.

Because `$regex` runs inside the MongoDB database engine, the database only returns the qualifying documents across the network.

---

## 5. Concurrency & Atomic Updates (Library Management)

When multiple clients interact with a database simultaneously, naive "read-then-write" logic causes **race conditions**.

### The Race Condition Flaw (Don't do this!):
```javascript
// Step 1: Read book from DB
const book = await booksCol.findOne({ title: "Clean Code" });

// Step 2: Check copies in JavaScript
if (book.copies > 0) {
  // Step 3: Write updated copies back
  await booksCol.updateOne({ title: "Clean Code" }, { $set: { copies: book.copies - 1 } });
}
```
If two users request the last remaining copy simultaneously:
1. User A reads: `copies = 1` (valid).
2. User B reads: `copies = 1` (valid).
3. User A updates: `copies = 0`.
4. User B updates: `copies = -1` (DATA CORRUPTION!).

---

### The Atomic Solution (Assignment 7 Implementation):
We use `findOneAndUpdate` with a query condition and the `$inc` operator:

```javascript
const result = await booksCol.findOneAndUpdate(
  {
    title: /^Clean Code$/i,
    copies: { $gt: 0 }  // Condition: Must have at least 1 copy available!
  },
  {
    $inc: { copies: -1 } // Atomic decrement
  },
  {
    returnDocument: "after"
  }
);
```

### Why this is 100% Thread-Safe:
1. MongoDB locks the individual document during the operation.
2. The check `{ copies: { $gt: 0 } }` and the decrement `{ $inc: { copies: -1 } }` happen in a **single atomic transaction** on the database server.
3. If `copies` is `0`, the query condition fails to match, the decrement never occurs, and `result` returns `null`.
4. `copies` can **never become negative**!
