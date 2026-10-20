# Assignment 6 — Hands-On Exercises: Step-by-Step Practical Tasks

These eight hands-on exercises are designed to test your understanding of MongoDB aggregations, driver methods, and Express REST routes through small, targeted modifications.

---

## Exercise 1: Change the `$match` Threshold in Branch Statistics
- **File to Edit:** `scripts/branch-above-60.js`
- **Intended Change:** Change the score filter from strictly greater than 60 (`$gt: 60`) to greater than or equal to 75 (`$gte: 75`).
- **Hint:** Locate the `$match` stage in the pipeline:
  ```javascript
  {
    $match: {
      marks: { $gte: 75 }
    }
  }
  ```
- **Expected Result:** Run `npm run branch-above-60`. Only students scoring 75 or higher (Aarav 88, Meera 94, Manish 78, Pooja 91) will be counted. CSE will show 2 and ECE will show 2. EEE will not appear because neither Vikram (72) nor Neha (65) reaches 75.

---

## Exercise 2: Add Department Head of Department (HOD) Email in Seeder & Lookup
- **Files to Edit:** `scripts/seed.js` and `scripts/lookup-students.js`
- **Intended Change:** Add an `email` field to each department in `seed.js` (e.g. `cse_hod@gitam.edu`) and project it in `lookup-students.js`.
- **Hint:**
  1. In `seed.js`, add `email: "cse_hod@univ.edu"` inside `departments`.
  2. In `lookup-students.js`, add `hodEmail: "$departmentDetails.email"` inside `$project`.
- **Expected Result:** Re-run `npm run seed` and `npm run lookup`. The output table will now include a `hodEmail` column.

---

## Exercise 3: Sort Subject Summary by Average Marks Descending
- **File to Edit:** `scripts/subject-summary.js`
- **Intended Change:** Instead of sorting by `rollNo: 1`, sort students by their calculated `averageSubjectMarks: -1` (highest average subject score first).
- **Hint:** Change the `$sort` stage at the end of the pipeline:
  ```javascript
  {
    $sort: { averageSubjectMarks: -1 }
  }
  ```
- **Expected Result:** Run `npm run subject-summary`. Meera Nair (94 avg) will appear at the top, followed by Pooja Reddy (91 avg).

---

## Exercise 4: Add Input Validation for Negative Marks in POST Route
- **File to Edit:** `api/server.js`
- **Intended Change:** Ensure that if a user sends `marks > 100` or `marks < 0`, the API immediately returns `400 Bad Request` with message `"Marks must be between 0 and 100"`.
- **Hint:** Look at the validation block inside `app.post("/students", ...)`:
  ```javascript
  if (marks !== undefined && (typeof marks !== "number" || marks < 0 || marks > 100)) {
    return res.status(400).json({ error: "Validation failed: 'marks' must be between 0 and 100." });
  }
  ```
- **Expected Result:** Send a POST request with `marks = 150`. The server will return HTTP 400 Bad Request instead of saving the invalid score.

---

## Exercise 5: Add a Custom `GET /branches` Aggregation Endpoint to the Express API
- **File to Edit:** `api/server.js`
- **Intended Change:** Add a new route `GET /branches` that runs the branch statistics pipeline and returns JSON containing branch averages.
- **Hint:** Add this route before the generic 404 handler:
  ```javascript
  app.get("/branches", async (req, res) => {
    const stats = await studentsCol.aggregate([
      { $group: { _id: "$branch", avgMarks: { $avg: "$marks" } } },
      { $project: { _id: 0, branch: "$_id", avgMarks: { $round: ["$avgMarks", 2] } } }
    ]).toArray();
    res.json(stats);
  });
  ```
- **Expected Result:** Start the server (`npm start`) and visit `http://localhost:3002/branches` in your browser or PowerShell. You will receive dynamic JSON with branch statistics.

---

## Exercise 6: Display the Lowest Subject Score in Subject Summary
- **File to Edit:** `scripts/subject-summary.js`
- **Intended Change:** Add `$min: "$subjects.marks"` as `lowestSubjectMarks` to the `$group` and `$project` stages.
- **Hint:** In the `$group` stage, add:
  ```javascript
  lowestSubjectMarks: { $min: "$subjects.marks" }
  ```
  And in `$project`, include `lowestSubjectMarks: 1`.
- **Expected Result:** Running `npm run subject-summary` will display an extra column showing each student's lowest individual subject score.

---

## Exercise 7: Make the REST API Return the Department Details on `GET /students`
- **File to Edit:** `api/server.js`
- **Intended Change:** Update `GET /students` to use `studentsCol.aggregate(...)` with the `$lookup` pipeline from `lookup-students.js` instead of plain `find({})`.
- **Hint:** Replace `find({}).toArray()` with:
  ```javascript
  const pipeline = [
    { $lookup: { from: "departments", localField: "departmentId", foreignField: "_id", as: "department" } },
    { $unwind: "$department" }
  ];
  const students = await studentsCol.aggregate(pipeline).toArray();
  ```
- **Expected Result:** Querying `http://localhost:3002/students` will include the full department sub-document inside each student object.

---

## Exercise 8: Test What Happens When an Invalid ObjectId is Passed to `PUT /students/:rollNo`
- **File to Run:** PowerShell
- **Intended Change:** Send a PUT request with `departmentId: "invalid-id-123"`.
- **Command:**
  ```powershell
  $body = @{ departmentId = "not-a-valid-id" } | ConvertTo-Json
  Invoke-RestMethod -Method PUT -Uri "http://localhost:3002/students/101" -ContentType "application/json" -Body $body
  ```
- **Expected Result:** The API returns `HTTP 400 Bad Request` with message: `"Validation failed: 'departmentId' is not a valid 24-character hexadecimal ObjectId."` and prevents server crash.
