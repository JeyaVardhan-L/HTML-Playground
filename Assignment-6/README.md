# Web Application Frameworks (WAF) — Lab Assignment 6
## MongoDB Lookup, Aggregation Pipelines & Express REST API

**Subject:** Web Application Frameworks (WAF) Lab  
**Assignment:** Lab Assignment 6 — MongoDB, Aggregation Pipelines & Express REST API  
**Technologies:** Node.js, Express.js (v4), MongoDB Native Driver (`mongodb` v6), JavaScript (ES2022)  
**Database Name:** `waf_assignment_6`  
**API Port:** `3002` (prevents conflict with Assignment 4 port 3000 & Assignment 5 port 3001)  
**Student:** Student Name · Department of Computer Science & Engineering (CSE), 3rd Year  

---

## 1. Assignment Purpose

This lab practical demonstrates how modern web applications integrate **Node.js** with a **MongoDB** document database using the official native MongoDB Node.js driver (`mongodb`). Rather than using heavy object-document mappers like Mongoose, this project emphasizes:

1. **Relational NoSQL Joins (`$lookup`):** Joining documents across collections on primary/foreign keys.
2. **Array Processing (`$unwind`):** Splitting nested arrays into individual document rows for calculations.
3. **Statistical Aggregations (`$group`):** Grouping records and calculating sums, averages, maximums, and minimums.
4. **Filtered Grouping (`$match`):** Combining query filters with grouping to extract targeted branch counts.
5. **Robust Express REST API:** Creating standard HTTP endpoints (`GET`, `POST`, `PUT`, `DELETE`) with request validation, unique index enforcement, and graceful shutdown handling.

---

## 2. Requirement-to-File Mapping

| Requirement | Description | Target File | npm Command |
| :--- | :--- | :--- | :--- |
| **Req 1** | `$lookup`: Join students with departments collection | [`scripts/lookup-students.js`](file:///c:/Users/user/Downloads/HTML-Playground/HTML-Playground/Assignment-6/scripts/lookup-students.js) | `npm run lookup` |
| **Req 2** | Express REST API using the native MongoDB driver | [`api/server.js`](file:///c:/Users/user/Downloads/HTML-Playground/HTML-Playground/Assignment-6/api/server.js) | `npm start` |
| **Req 3** | `$unwind` & `$group`: Total and average subject marks per student | [`scripts/subject-summary.js`](file:///c:/Users/user/Downloads/HTML-Playground/HTML-Playground/Assignment-6/scripts/subject-summary.js) | `npm run subject-summary` |
| **Req 4** | `$match` then `$group`: Count students scoring > 60 by branch | [`scripts/branch-above-60.js`](file:///c:/Users/user/Downloads/HTML-Playground/HTML-Playground/Assignment-6/scripts/branch-above-60.js) | `npm run branch-above-60` |
| **Req 5** | Branch-wise average, maximum, and minimum marks (sorted desc) | [`scripts/branch-statistics.js`](file:///c:/Users/user/Downloads/HTML-Playground/HTML-Playground/Assignment-6/scripts/branch-statistics.js) | `npm run branch-statistics` |
| **Seed** | Idempotent seeder: 3 departments & 8 students | [`scripts/seed.js`](file:///c:/Users/user/Downloads/HTML-Playground/HTML-Playground/Assignment-6/scripts/seed.js) | `npm run seed` |

---

## 3. Directory Structure

```text
Assignment-6/
├── README.md                      ← Overview, commands, API documentation & checklist
├── package.json                   ← Declares express, mongodb driver & npm script shortcuts
├── .gitignore                     ← Ignores node_modules/ and local environment files
├── api/
│   └── server.js                  ← Requirement 2: Express REST API on Port 3002
├── scripts/
│   ├── seed.js                    ← Idempotent seeder (departments & students)
│   ├── lookup-students.js         ← Requirement 1: $lookup and $unwind join
│   ├── subject-summary.js         ← Requirement 3: $unwind and $group on subjects
│   ├── branch-above-60.js         ← Requirement 4: $match and $group for marks > 60
│   └── branch-statistics.js       ← Requirement 5: Branch $avg, $max, $min sorted desc
└── docs/
    └── learning/
        ├── START-HERE.md          ← Orientation, architecture diagrams & study plan
        ├── MONGODB-FROM-ZERO.md   ← Core NoSQL concepts, BSON, ObjectId & CRUD
        ├── EXPRESS-REST-API.md    ← REST architecture, routes, status codes & validation
        ├── AGGREGATION-EXPLAINED.md ← Pipeline stages ($lookup, $unwind, $group, $match)
        ├── CODE-EXPLANATION.md    ← Line-by-line breakdown of every file & query
        ├── VIVA-PREP.md           ← 20 high-yield viva questions with spoken model answers
        ├── HANDS-ON-EXERCISES.md  ← 8 beginner hands-on coding exercises
        └── GLOSSARY.md            ← Definitions of key NoSQL and web terminology
```

---

## 4. Prerequisites & Free Local MongoDB Setup

Before running this assignment, ensure **Node.js** (v18 or higher) and **npm** are installed.

```powershell
node -v
npm -v
```

### Free Local MongoDB Community Server Setup (Windows)

This assignment requires a running MongoDB server instance. MongoDB Community Server is **100% free and open-source**:

#### Option A: Install via Windows Package Manager (winget)
Open an Administrator PowerShell terminal and run:
```powershell
winget install MongoDB.Server
```

#### Option B: Download the Official Installer (MSI)
1. Visit the official MongoDB Community download page:  
   `https://www.mongodb.com/try/download/community`
2. Select **Version: Current**, **Platform: Windows (x64)**, **Package: msi**.
3. Run the installer and choose **"Complete"** installation. Ensure **"Install MongoDB as a Service"** is checked.
4. Once installed, MongoDB will run as a Windows background service listening on `localhost:27017`.

#### Verify or Start MongoDB Service
```powershell
# Check if MongoDB service is running
Get-Service -Name MongoDB -ErrorAction SilentlyContinue

# Start the service if stopped
net start MongoDB
```

---

## 5. Installation & Database Seeding (PowerShell)

### Step 1: Navigate to the Assignment 6 Directory
```powershell
cd c:\Users\user\Downloads\HTML-Playground\HTML-Playground\Assignment-6
```

### Step 2: Install Project Dependencies
```powershell
npm install
```

### Step 3: Seed the Database
```powershell
npm run seed
```
*(Runs [`scripts/seed.js`](file:///c:/Users/user/Downloads/HTML-Playground/HTML-Playground/Assignment-6/scripts/seed.js) idempotently)*

---

## 6. How to Run Each Task & Expected Outputs

### Task 1: `$lookup` Students and Departments (Requirement 1)
```powershell
npm run lookup
```
**Expected Output:**
```text
================================================================================
Requirement 1: MongoDB Aggregation — $lookup Join (Students + Departments)
================================================================================

Found 8 students joined with department details:

┌─────────┬────────┬────────────────┬────────┬──────────────────────────────────────────┬─────────────────┐
│ (index) │ rollNo │ name           │ branch │ departmentName                           │ hod             │
├─────────┼────────┼────────────────┼────────┼──────────────────────────────────────────┼─────────────────┤
│ 0       │ '101'  │ 'Aarav Sharma' │ 'CSE'  │ 'Computer Science & Engineering'         │ 'Dr. K. S. Rao' │
│ 1       │ '102'  │ 'Meera Nair'   │ 'CSE'  │ 'Computer Science & Engineering'         │ 'Dr. K. S. Rao' │
│ 2       │ '103'  │ 'Rohan Varma'  │ 'CSE'  │ 'Computer Science & Engineering'         │ 'Dr. K. S. Rao' │
│ 3       │ '104'  │ 'Manish Gupta' │ 'ECE'  │ 'Electronics & Communication Engineering' │ 'Dr. P. Sharma' │
│ 4       │ '105'  │ 'Pooja Reddy'  │ 'ECE'  │ 'Electronics & Communication Engineering' │ 'Dr. P. Sharma' │
│ 5       │ '106'  │ 'Suresh Iyer'  │ 'ECE'  │ 'Electronics & Communication Engineering' │ 'Dr. P. Sharma' │
│ 6       │ '107'  │ 'Vikram Das'   │ 'EEE'  │ 'Electrical & Electronics Engineering'   │ 'Dr. R. V. Raman'│
│ 7       │ '108'  │ 'Neha Patel'   │ 'EEE'  │ 'Electrical & Electronics Engineering'   │ 'Dr. R. V. Raman'│
└─────────┴────────┴────────────────┴────────┴──────────────────────────────────────────┴─────────────────┘
```

---

### Task 2: Subject Marks Summary (`$unwind` & `$group`) (Requirement 3)
```powershell
npm run subject-summary
```
**Expected Output:**
```text
================================================================================
Requirement 3: MongoDB Aggregation — $unwind & $group (Subject Marks Summary)
================================================================================

Calculated subject summary for 8 students:

┌─────────┬────────┬────────────────┬────────┬──────────────┬───────────────────┬─────────────────────┐
│ (index) │ rollNo │ name           │ branch │ subjectCount │ totalSubjectMarks │ averageSubjectMarks │
├─────────┼────────┼────────────────┼────────┼──────────────┼───────────────────┼─────────────────────┤
│ 0       │ '101'  │ 'Aarav Sharma' │ 'CSE'  │ 2            │ 176               │ 88                  │
│ 1       │ '102'  │ 'Meera Nair'   │ 'CSE'  │ 2            │ 188               │ 94                  │
│ 2       │ '103'  │ 'Rohan Varma'  │ 'CSE'  │ 2            │ 70                │ 35                  │
│ 3       │ '104'  │ 'Manish Gupta' │ 'ECE'  │ 2            │ 156               │ 78                  │
│ 4       │ '105'  │ 'Pooja Reddy'  │ 'ECE'  │ 2            │ 182               │ 91                  │
│ 5       │ '106'  │ 'Suresh Iyer'  │ 'ECE'  │ 2            │ 76                │ 38                  │
│ 6       │ '107'  │ 'Vikram Das'   │ 'EEE'  │ 2            │ 144               │ 72                  │
│ 7       │ '108'  │ 'Neha Patel'   │ 'EEE'  │ 2            │ 130               │ 65                  │
└─────────┴────────┴────────────────┴────────┴──────────────┴───────────────────┴─────────────────────┘
```

---

### Task 3: Branch Counts for Marks > 60 (`$match` & `$group`) (Requirement 4)
```powershell
npm run branch-above-60
```
**Expected Output:**
```text
================================================================================
Requirement 4: MongoDB Aggregation — $match & $group (Students with Marks > 60)
================================================================================

Branch-wise count of students scoring > 60:

┌─────────┬────────┬──────────────────────┐
│ (index) │ branch │ studentsAbove60Count │
├─────────┼────────┼──────────────────────┤
│ 0       │ 'CSE'  │ 2                    │
│ 1       │ 'ECE'  │ 2                    │
│ 2       │ 'EEE'  │ 2                    │
└─────────┴────────┴──────────────────────┘
```

---

### Task 4: Branch Statistics (`$avg`, `$max`, `$min` sorted desc) (Requirement 5)
```powershell
npm run branch-statistics
```
**Expected Output:**
```text
================================================================================
Requirement 5: MongoDB Aggregation — Branch-Wise Statistics ($avg, $max, $min)
================================================================================

Branch statistics calculated across 3 branches (sorted by avg desc):

┌─────────┬────────┬───────────────┬──────────────┬──────────┬──────────┐
│ (index) │ branch │ totalStudents │ averageMarks │ maxMarks │ minMarks │
├─────────┼────────┼───────────────┼──────────────┼──────────┼──────────┤
│ 0       │ 'CSE'  │ 3             │ 72.33        │ 94       │ 35       │
│ 1       │ 'ECE'  │ 3             │ 69           │ 91       │ 38       │
│ 2       │ 'EEE'  │ 2             │ 68.5         │ 72       │ 65       │
└─────────┴────────┴───────────────┴──────────────┴──────────┴──────────┘
```

---

## 7. Express REST API Demonstration (Requirement 2)

### Starting the Server
```powershell
npm start
```
Terminal display:
```text
==================================================
Express REST API running on http://localhost:3002
Connected to MongoDB Database: "waf_assignment_6"
Collection: "students" (unique index on rollNo enforced)
Ready to accept API requests.
==================================================
```

### Testing Endpoints Using PowerShell `Invoke-RestMethod`

#### 1. List All Students (`GET /students`)
```powershell
Invoke-RestMethod -Uri "http://localhost:3002/students" | Format-Table rollNo, name, branch, marks
```

#### 2. Get One Student by Roll Number (`GET /students/:rollNo`)
```powershell
Invoke-RestMethod -Uri "http://localhost:3002/students/101"
```
**Sample Response:**
```json
{
  "_id": "65f1b2b2b2b2b2b2b2b2b101",
  "rollNo": "101",
  "name": "Aarav Sharma",
  "branch": "CSE",
  "departmentId": "65f1a1a1a1a1a1a1a1a1a101",
  "marks": 88,
  "subjects": [
    { "name": "DBMS", "marks": 90 },
    { "name": "JavaScript", "marks": 86 }
  ]
}
```

#### 3. Add a New Student (`POST /students`)
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
**Sample Response (HTTP 201 Created):**
```json
{
  "message": "Student created successfully",
  "student": {
    "_id": "...",
    "rollNo": "109",
    "name": "Ananya Sen",
    "branch": "CSE",
    "departmentId": null,
    "marks": 86,
    "subjects": [
      { "name": "DBMS", "marks": 88 },
      { "name": "JavaScript", "marks": 84 }
    ]
  }
}
```

#### 4. Update Student (`PUT /students/:rollNo`)
```powershell
$update = @{
  marks = 92
  name = "Ananya Sen (Updated)"
} | ConvertTo-Json

Invoke-RestMethod -Method PUT -Uri "http://localhost:3002/students/109" -ContentType "application/json" -Body $update
```
**Sample Response (HTTP 200 OK):**
```json
{
  "message": "Student '109' updated successfully.",
  "student": {
    "rollNo": "109",
    "name": "Ananya Sen (Updated)",
    "marks": 92
  }
}
```

#### 5. Delete Student (`DELETE /students/:rollNo`)
```powershell
Invoke-RestMethod -Method DELETE -Uri "http://localhost:3002/students/109"
```
**Sample Response (HTTP 200 OK):**
```json
{
  "message": "Student '109' was deleted successfully.",
  "deletedRollNo": "109"
}
```

---

## 8. Verification Checklist

- [x] Dependencies install cleanly via `npm install`.
- [x] `npm run seed` idempotently creates/updates 3 departments and 8 students.
- [x] Unique index created on `students(rollNo)`.
- [x] `npm run lookup` executes `$lookup` and `$unwind` join between students and departments.
- [x] `npm run subject-summary` deconstructs `subjects` array and computes sum & avg per student.
- [x] `npm run branch-above-60` filters `marks > 60` with `$match` and counts by branch.
- [x] `npm run branch-statistics` computes `$avg`, `$max`, `$min` grouped by branch, sorted descending by average.
- [x] Express REST API runs on port `3002` without conflicting with port 3000 or 3001.
- [x] All 5 REST routes implemented with validation and proper HTTP status codes (200, 201, 400, 404, 500).
- [x] Graceful shutdown registered on `SIGINT` and `SIGTERM`.

---

## 9. Common Errors & Troubleshooting

### Error: `ECONNREFUSED 127.0.0.1:27017`
- **Cause:** The local MongoDB service is not started.
- **Solution:** Run `net start MongoDB` in an Administrator PowerShell window or start `mongod.exe`.

### Error: `Port 3002 is already in use (EADDRINUSE)`
- **Cause:** Another process is occupying port 3002.
- **Solution:** Stop the process using `Get-Process -Id (Get-NetTCPConnection -LocalPort 3002).OwningProcess | Stop-Process -Force` or start the server on a different port: `$env:PORT=3005; npm start`.

### Error: `Duplicate key error (code 11000)`
- **Cause:** Attempting to insert a student with an already existing `rollNo`.
- **Solution:** The API automatically translates code 11000 into a friendly HTTP 400 Bad Request error. Provide a unique roll number.
