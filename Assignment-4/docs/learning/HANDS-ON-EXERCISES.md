# Hands-On Practice Exercises

This guide contains **12 beginner-friendly hands-on exercises** designed to build practical confidence. Each exercise asks you to make a small, focused modification to an existing file in `Assignment-4/` without rewriting the entire program.

For every exercise, you will find:
1. **Target File** — the exact file to open.
2. **Intended Change** — what feature or data to alter.
3. **Small Hint** — code guidance pointing to the exact line or block.
4. **Expected Result** — what you should observe in your terminal or browser.

---

## Exercise Index

| # | Topic | File | Difficulty |
|:---|:---|:---|:---|
| **Ex 1** | Change Student Data in Express API | `express-fetch/server.js` | 🟢 Easy |
| **Ex 2** | Add a Field to the Express Response & UI | `server.js` & `public/index.html` | 🟢 Easy |
| **Ex 3** | Change the Heading & Button Text in Fetch UI | `express-fetch/public/index.html` | 🟢 Easy |
| **Ex 4** | Customize Student Details in Function Component | `react-practicals/src/components/FunctionStudent.jsx` | 🟢 Easy |
| **Ex 5** | Customize Student Bio in Class Component | `react-practicals/src/components/ClassStudent.jsx` | 🟢 Easy |
| **Ex 6** | Change Counter Step Size to +5 / -5 | `react-practicals/src/components/StateCounter.jsx` | 🟡 Medium |
| **Ex 7** | Prevent Negative Counter Values | `react-practicals/src/components/StateCounter.jsx` | 🟡 Medium |
| **Ex 8** | Add a Third Student to Props Demonstration | `react-practicals/src/components/StudentProps.jsx` | 🟢 Easy |
| **Ex 9** | Pass a New Prop (`rollNo`) from Parent to Child | `react-practicals/src/components/StudentProps.jsx` | 🟡 Medium |
| **Ex 10** | Modify the Document Title in `useEffect` | `react-practicals/src/components/HooksDemo.jsx` | 🟢 Easy |
| **Ex 11** | Add a "Clear Text" Button in Hooks Demo | `react-practicals/src/components/HooksDemo.jsx` | 🟡 Medium |
| **Ex 12** | Test Backend Failure & Error Handling | `express-fetch/public/index.html` | 🟡 Medium |

---

## Exercise 1: Change Student Data in Express API
- **Target File:** `express-fetch/server.js`
- **Intended Change:** Change the hardcoded student name from `"Aarav Sharma"` to your own name, and change the roll number to your college roll number.
- **Hint:** Locate the `studentData` constant near lines 13–19:
  ```javascript
  const studentData = {
    name: "Your Name Here",
    rollNumber: "2024-WAF-099",
    branch: "Computer Science and Engineering",
    academicYear: "3rd Year",
    status: "Active"
  };
  ```
- **Expected Result:**  
  1. Restart the Express server (`node server.js`).
  2. Open `http://localhost:3000` and click **"Fetch Data"**.
  3. The card should immediately display your name and new roll number.

---

## Exercise 2: Add a Field to the Express Response & UI
- **Target File:** `express-fetch/server.js` and `express-fetch/public/index.html`
- **Intended Change:** Add a `"cgpa"` field (e.g. `"9.20"`) to the server response and display it on the webpage.
- **Hint:**
  1. In `server.js`, add `cgpa: "9.20"` to `studentData`.
  2. In `public/index.html`, add another row inside the `dataDisplay.innerHTML` template string:
  ```javascript
  <div class="info-row">
    <span class="info-label">CGPA:</span>
    <span class="info-value">${data.cgpa}</span>
  </div>
  ```
- **Expected Result:** Clicking "Fetch Data" renders a new line showing **CGPA: 9.20**.

---

## Exercise 3: Change the Heading & Button Text in Fetch UI
- **Target File:** `express-fetch/public/index.html`
- **Intended Change:** Change the page heading to `"College Web Portal"` and the button text to `"Load Student Record"`.
- **Hint:** Look at the HTML structure inside the `<div class="card">`:
  ```html
  <h2>College Web Portal</h2>
  <button id="fetchBtn" class="btn btn-primary">Load Student Record</button>
  ```
- **Expected Result:** Refresh `http://localhost:3000`. The card shows the updated heading and button label without touching any JavaScript.

---

## Exercise 4: Customize Student Details in Function Component
- **Target File:** `react-practicals/src/components/FunctionStudent.jsx`
- **Intended Change:** Change the displayed student's name, branch, and add a `"Section"` field in the function component.
- **Hint:** In `FunctionStudent.jsx`, add a new property to the `student` object:
  ```jsx
  const student = {
    name: "Aditi Rao",
    branch: "Information Technology",
    yearOfStudy: "3rd Year (Semester 5)",
    section: "Section B" // New field
  };
  ```
  Then display it inside the JSX:
  ```jsx
  <div className="info-row">
    <span className="info-label">Section:</span>
    <span className="info-value">{student.section}</span>
  </div>
  ```
- **Expected Result:** Save the file. Vite hot-reloads instantly, and Practical 6 shows the Section row.

---

## Exercise 5: Customize Student Bio in Class Component
- **Target File:** `react-practicals/src/components/ClassStudent.jsx`
- **Intended Change:** Update the class component's constructor state to reflect an interest in cloud computing.
- **Hint:** Look inside the `constructor(props)`:
  ```javascript
  this.state = {
    studentName: "Priya Patel",
    rollNumber: "CS-2024-042",
    description: "Aspiring Cloud Solutions Architect with a passion for serverless microservices and distributed databases."
  };
  ```
- **Expected Result:** Open the "Practical 3 (Class Component)" tab. The bio paragraph updates immediately.

---

## Exercise 6: Change Counter Step Size to +5 / -5
- **Target File:** `react-practicals/src/components/StateCounter.jsx`
- **Intended Change:** Make the counter increase and decrease by 5 on every click instead of 1.
- **Hint:** Locate the `handleIncrement` and `handleDecrement` functions:
  ```javascript
  const handleIncrement = () => setCount(prevCount => prevCount + 5);
  const handleDecrement = () => setCount(prevCount => prevCount - 5);
  ```
  Update the button text from `+1` to `+5` and `-1` to `-5`.
- **Expected Result:** Clicking the increment button advances the count from 0 to 5, 10, 15, and the decrement button lowers it by 5.

---

## Exercise 7: Prevent Negative Counter Values
- **Target File:** `react-practicals/src/components/StateCounter.jsx`
- **Intended Change:** Modify the decrement function so the counter cannot go below zero.
- **Hint:** Add an `if` check inside `handleDecrement`:
  ```javascript
  const handleDecrement = () => {
    setCount(prevCount => (prevCount > 0 ? prevCount - 1 : 0));
  };
  ```
- **Expected Result:** When the counter is at 0, clicking `- 1` keeps the count at 0.

---

## Exercise 8: Add a Third Student to Props Demonstration
- **Target File:** `react-practicals/src/components/StudentProps.jsx`
- **Intended Change:** Add a third student (e.g. `"Vikram Mehta"`, `"Mechanical Engineering"`) to the parent component's array.
- **Hint:** Open `StudentProps.jsx` and add a third object to `studentsList`:
  ```javascript
  const studentsList = [
    { id: 1, name: "Sneha Roy", branch: "Computer Science and Engineering", rollNo: "CSE-101" },
    { id: 2, name: "Kabir Verma", branch: "Electronics and Communication", rollNo: "ECE-204" },
    { id: 3, name: "Vikram Mehta", branch: "Mechanical Engineering", rollNo: "ME-312" }
  ];
  ```
- **Expected Result:** Practical 4 automatically renders three student cards instead of two because `.map()` iterates over the entire array dynamically!

---

## Exercise 9: Pass a New Prop (`rollNo`) from Parent to Child
- **Target File:** `react-practicals/src/components/StudentProps.jsx`
- **Intended Change:** Pass each student's `rollNo` from the parent to `<StudentCard />` and display it in the child component.
- **Hint:**
  1. In the parent component's `.map()`, pass `rollNo={student.rollNo}`:
  ```jsx
  <StudentCard
    key={student.id}
    name={student.name}
    branch={student.branch}
    rollNo={student.rollNo}
  />
  ```
  2. In `function StudentCard({ name, branch, rollNo })`, render the new prop:
  ```jsx
  <div className="info-row">
    <span className="info-label">Roll Number:</span>
    <span className="info-value">{rollNo}</span>
  </div>
  ```
- **Expected Result:** Every student card in Practical 4 now displays their roll number alongside their name and branch.

---

## Exercise 10: Modify the Document Title in `useEffect`
- **Target File:** `react-practicals/src/components/HooksDemo.jsx`
- **Intended Change:** Change the browser tab title format to show an emoji and the word "Clicks": `"🔥 Clicks: X | React Lab"`.
- **Hint:** Update the string inside `useEffect`:
  ```javascript
  useEffect(() => {
    document.title = `🔥 Clicks: ${hookCount} | React Lab`;
    return () => {
      document.title = "Assignment 4 - React Practicals";
    };
  }, [hookCount]);
  ```
- **Expected Result:** Whenever you click the "Increase (+1)" button in Practical 5, observe your browser tab bar update to `"🔥 Clicks: 1 | React Lab"`, `"🔥 Clicks: 2 | React Lab"`, etc.

---

## Exercise 11: Add a "Clear Text" Button in Hooks Demo
- **Target File:** `react-practicals/src/components/HooksDemo.jsx`
- **Intended Change:** Add a "Clear" button that empties the text input and resets `textValue` to `""`.
- **Hint:**
  1. Add a handler function:
  ```javascript
  const handleClear = () => {
    setTextValue("");
    if (inputRef.current) {
      inputRef.current.focus(); // Bonus: keep the focus active!
    }
  };
  ```
  2. Add the button to the JSX near the "Focus Input" button:
  ```jsx
  <button onClick={handleClear} className="btn btn-secondary">
    Clear Text
  </button>
  ```
- **Expected Result:** Typing text and clicking "Clear Text" clears the input field immediately and places the blinking cursor right back inside the input.

---

## Exercise 12: Test Backend Failure & Error Handling
- **Target File:** `express-fetch/public/index.html`
- **Intended Change:** Temporarily change the fetch URL to an invalid endpoint (`/api/nonexistent`) to test how the browser displays errors.
- **Hint:** In `public/index.html`, modify line ~68:
  ```javascript
  // Change '/api/student' to a wrong route:
  const response = await fetch('/api/nonexistent');
  ```
- **Expected Result:**  
  1. Save `index.html` and refresh `http://localhost:3000`.
  2. Click **"Fetch Data"**.
  3. Instead of crashing, the UI cleanly renders:  
     `"❌ Server responded with HTTP error 404"` in red.
  4. Change it back to `/api/student` to restore normal behavior.
