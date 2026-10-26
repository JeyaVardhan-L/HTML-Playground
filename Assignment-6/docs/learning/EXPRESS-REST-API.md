# Express REST API Architecture: Design, Validation & MongoDB Integration

This guide walks through the architectural patterns, HTTP mechanics, and database design implemented in `Assignment-6/api/server.js`.

---

## 1. What is a RESTful API?

**REST** stands for **Representational State Transfer**. It is a software architectural style for distributed hypermedia systems. In practical web development, a REST API uses the standard HTTP protocol to expose CRUD (Create, Read, Update, Delete) operations over resources (such as students).

### The CRUD-to-HTTP Mapping

| Operation | HTTP Method | Route | Idempotent? | Status Code | Purpose |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Create** | `POST` | `/students` | No | `201 Created` | Insert a new student |
| **Read All** | `GET` | `/students` | Yes | `200 OK` | List all student records |
| **Read One**| `GET` | `/students/:rollNo` | Yes | `200 OK` / `404` | Retrieve student by roll number |
| **Update**  | `PUT` | `/students/:rollNo` | Yes | `200 OK` / `400` / `404` | Update student attributes |
| **Delete**  | `DELETE` | `/students/:rollNo` | Yes | `200 OK` / `404` | Remove student from database |

---

## 2. Express Server Architecture (`api/server.js`)

```text
[ Client (PowerShell / Browser) ]
               |
               v HTTP Request (e.g. POST /students + JSON Body)
+-------------------------------------------------------------+
|                      Express.js App                         |
|                                                             |
|  1. express.json() Middleware                               |
|     - Reads incoming raw stream                             |
|     - Parses JSON into req.body                             |
|                                                             |
|  2. Router Matching                                         |
|     - Matches method + path (/students)                     |
|                                                             |
|  3. Route Handler Logic                                     |
|     - Validates rollNo, name, marks                         |
|     - Checks for duplicate roll number                      |
|     - Issues MongoDB Command via native driver              |
|                                                             |
|  4. Response Generation                                     |
|     - Sends HTTP status (201 / 400 / 404 / 500)             |
|     - Serializes response payload into JSON string          |
+-------------------------------------------------------------+
               |
               v Wire Protocol (TCP)
[ MongoDB Community Server: Database "waf_assignment_6", Collection "students" ]
```

---

## 3. Detailed Route Breakdown

### 1. `POST /students` — Create Student
- **Input:** Request body containing `rollNo`, `name`, optional `branch`, `departmentId`, `marks`, `subjects`.
- **Validation:**
  - `rollNo`: non-empty string.
  - `name`: non-empty string.
  - `marks`: number between 0 and 100 if supplied.
  - `departmentId`: valid 24-character hexadecimal `ObjectId` string if supplied.
- **Duplicate Prevention:**
  1. Application-level check: `studentsCol.findOne({ rollNo })` returns `400 Bad Request`.
  2. Database-level safety net: unique index on `rollNo` catches any race condition (error code `11000`).
- **Response:** `201 Created` with the inserted document including its new `_id`.

### 2. `GET /students` — List All Students
- Queries `studentsCol.find({}).sort({ rollNo: 1 }).toArray()`.
- **Response:** `200 OK` with JSON array.

### 3. `GET /students/:rollNo` — Retrieve by Roll Number
- Extracts `req.params.rollNo`.
- Queries `studentsCol.findOne({ rollNo })`.
- If found: returns `200 OK` with student object.
- If not found: returns `404 Not Found` with `{ error: "Student with roll number '...' was not found." }`.

### 4. `PUT /students/:rollNo` — Update Student
- Uses `studentsCol.findOneAndUpdate({ rollNo }, { $set: updates }, { returnDocument: "after" })`.
- **Safety Rules:**
  - Strips `_id` from the update payload to prevent attempting to modify MongoDB's immutable primary key.
  - Validates `marks` if provided.
  - If the student attempts to change their `rollNo` to an already-existing roll number, rejects with `400 Bad Request`.
- If no record matches: returns `404 Not Found`.
- On success: returns `200 OK` with updated student document.

### 5. `DELETE /students/:rollNo` — Delete Student
- Calls `studentsCol.deleteOne({ rollNo })`.
- Inspects `result.deletedCount`:
  - `0`: No document matched → returns `404 Not Found`.
  - `1`: Document deleted → returns `200 OK` with `{ message: "...", deletedRollNo: "..." }`.

---

## 4. HTTP Status Codes Explained

| Code | Standard Label | Meaning in this API |
| :--- | :--- | :--- |
| **`200`** | `OK` | Request succeeded (GET, PUT, or DELETE). |
| **`201`** | `Created` | New student document was successfully created (POST). |
| **`400`** | `Bad Request` | Client sent malformed data (missing rollNo/name, negative marks, duplicate rollNo). |
| **`404`** | `Not Found` | Target student does not exist, or unhandled URL endpoint. |
| **`500`** | `Internal Server Error` | Unhandled database connection or driver failure. |

---

## 5. Graceful Server Shutdown

When a developer stops a Node.js server with `Ctrl+C`, the process receives a `SIGINT` (Signal Interrupt) event. If unhandled, active client requests can be abruptly aborted and database sockets can remain hanging.

In `api/server.js`, we listen for `SIGINT` and `SIGTERM`:
```javascript
async function shutdown(signal) {
  console.log(`\nReceived ${signal}. Shutting down gracefully...`);
  if (server) {
    server.close(() => console.log("HTTP server closed."));
  }
  if (client) {
    await client.close();
    console.log("MongoDB connection closed.");
  }
  process.exit(0);
}

process.on("SIGINT", () => shutdown("SIGINT"));
process.on("SIGTERM", () => shutdown("SIGTERM"));
```

---

## 6. Testing the API with PowerShell

### Add a New Student (`POST /students`)
```powershell
$body = @{
  rollNo = "109"
  name = "Ananya Sen"
  branch = "CSE"
  marks = 86
  subjects = @(
    @{ name = "DBMS"; marks = 88 },
    @{ name = "JavaScript"; marks = 84 }
  )
} | ConvertTo-Json -Depth 5

Invoke-RestMethod -Method POST -Uri "http://localhost:3002/students" -ContentType "application/json" -Body $body
```

### List All Students (`GET /students`)
```powershell
Invoke-RestMethod -Uri "http://localhost:3002/students" | Format-Table rollNo, name, branch, marks
```

### Get One Student by Roll Number (`GET /students/101`)
```powershell
Invoke-RestMethod -Uri "http://localhost:3002/students/101"
```

### Update Student (`PUT /students/109`)
```powershell
$update = @{
  marks = 92
  name = "Ananya Sen (Updated)"
} | ConvertTo-Json

Invoke-RestMethod -Method PUT -Uri "http://localhost:3002/students/109" -ContentType "application/json" -Body $update
```

### Delete Student (`DELETE /students/109`)
```powershell
Invoke-RestMethod -Method DELETE -Uri "http://localhost:3002/students/109"
```
