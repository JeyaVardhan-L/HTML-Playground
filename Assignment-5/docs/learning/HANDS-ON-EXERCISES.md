# Assignment 5 — Hands-On Exercises: Step-by-Step Practical Tasks

These six hands-on exercises will help reinforce your understanding of how the client and server interact. Each exercise requires only a small, specific edit and does not require rewriting the project.

---

## Exercise 1: Customize the Student Name and Details

- **File to Edit:** `Assignment-5/server.js`
- **Intended Change:** Change the default student values from "Student Name" to your own name, branch, and year.
- **Hint:** Locate the `studentData` object near line 20:
  ```javascript
  const studentData = {
    name: "Student Name",
    branch: "CSE",
    year: "3rd Year"
  };
  ```
- **Expected Result:** Save `server.js`, restart the server (`Ctrl+C` then `node server.js`), refresh the page at `http://localhost:3001`, and click **Fetch Data**. The table will now display your custom student information.

---

## Exercise 2: Add a "College / University" Field to the Data

- **File to Edit:** `Assignment-5/server.js` and `Assignment-5/public/index.html`
- **Intended Change:** Add a new property called `university: "GITAM University"` to the backend response and display it in the frontend table.
- **Hint:**
  1. In `server.js`, add `university: "GITAM University"` to `studentData` and include `university: studentData.university` inside `res.json({ ... })`.
  2. In `public/index.html`, add a new list item inside `<ul class="info-list">`:
     ```html
     <li>
       <span class="il-label">University</span>
       <span class="il-value" id="studentUniversity">—</span>
     </li>
     ```
  3. In `index.html` script, add:
     ```javascript
     const studentUniversity = document.getElementById("studentUniversity");
     // inside fetchStudentData:
     studentUniversity.textContent = data.university;
     ```
- **Expected Result:** When you fetch data, the table displays a new "University" row with value "GITAM University".

---

## Exercise 3: Change the Button and Heading Text

- **File to Edit:** `Assignment-5/public/index.html`
- **Intended Change:** Change the button label from "Fetch Data" to "Request Fresh Student Record", and the heading to "Student API Connection Lab".
- **Hint:**
  - Find the `<h1>` tag inside `<header class="page-header">`.
  - Find the `<button id="fetchBtn">` element in the HTML.
- **Expected Result:** Refresh the browser page. The interface immediately reflects the new titles without needing to restart the backend Node.js server.

---

## Exercise 4: Format the Server Terminal Log Message

- **File to Edit:** `Assignment-5/server.js`
- **Intended Change:** Modify the terminal output format to include both the request number and the timestamp, e.g.:  
  `[SERVER LOG] Request #1 received at 5:35:10 PM`
- **Hint:** Look at the `console.log` line inside `app.get("/api/student", ...)`:
  ```javascript
  console.log(`[SERVER LOG] Request #${requestCount} received at ${timestamp}`);
  ```
- **Expected Result:** Restart the server. Each time you click the button in the browser, the terminal prints the new formatted log message.

---

## Exercise 5: Customize the Client Success Message

- **File to Edit:** `Assignment-5/public/index.html`
- **Intended Change:** Change the green success status message to show the response round-trip note:  
  `"Connection active: Received record for Student Name (Request #1)"`.
- **Hint:** Inside `fetchStudentData()` in `index.html`, locate the line setting `statusMessage.textContent`:
  ```javascript
  statusMessage.textContent = `Connection active: Received record for ${data.name} (Request #${data.requestNumber})`;
  ```
- **Expected Result:** When you click **Fetch Data**, the success badge above the table displays the custom formatted confirmation.

---

## Exercise 6: Simulate and Observe Network Error Handling

- **File to Edit:** None (Operational test)
- **Intended Change:** Verify that the frontend `try/catch` block correctly handles server downtime.
- **Steps:**
  1. Start the server with `node server.js` and open `http://localhost:3001` in your browser.
  2. Switch to your terminal and stop the server by pressing `Ctrl + C`.
  3. Go back to the browser and click the **Fetch Data** button.
- **Expected Result:** Instead of freezing or failing silently:
  - The loading message briefly appears.
  - A red error box appears saying: *"Failed to fetch data: Failed to fetch. Ensure the Express server is running on port 3001."*
  - The button is re-enabled so you can try again once the server is restarted.
