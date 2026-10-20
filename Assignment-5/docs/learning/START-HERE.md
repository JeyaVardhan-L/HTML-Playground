# Assignment 5 — Start Here: Beginner Orientation & Learning Roadmap

Welcome to **Assignment 5**! This guide is designed to help you understand every component of this practical from the ground up.

---

## 1. What This Practical Demonstrates

In modern web development, websites rarely reload the entire page just to show updated information. Instead, they use **asynchronous HTTP requests** to exchange data behind the scenes.

This assignment specifically illustrates:
1. **Client vs. Server Separation:** The browser acts as the client requesting data; Express.js acts as the server providing data.
2. **On-Demand Connections:** Unlike the initial connection that downloaded the HTML page, clicking the **Fetch Data** button opens a **new, independent HTTP connection** on every click.
3. **Dynamic Server-Side State:** The server keeps track of how many requests it has received (`requestCount`) and generates a fresh timestamp for each one.
4. **Terminal Observability:** Every time a client request reaches the Express server, a message is printed directly in the server's terminal (`GET /api/student: request 1`, `request 2`, etc.).

---

## 2. Roles of the Technologies

| Technology | Role | What It Does in This Project |
| :--- | :--- | :--- |
| **HTML** | Structure | Defines the page layout: the header, the explanation banner, the **Fetch Data** button, and the table for displaying student details. |
| **CSS** | Styling | Formats the page using a clean, student-built aesthetic with readable fonts, clear borders, and responsive spacing. |
| **Browser JavaScript** | Client Logic | Listens for button clicks, manages loading/error states, initiates `fetch('/api/student')`, and updates the DOM with the received data. |
| **Node.js** | Runtime | Allows JavaScript to run outside the browser as a desktop/server environment, enabling file reading and network socket management. |
| **Express.js** | Backend Framework | Runs on top of Node.js to create HTTP servers, route requests (`GET /`, `GET /api/student`), serve static files, and send JSON responses. |

---

## 3. Client and Server: The Core Concept

- **The Client (Web Browser):** The consumer. It requests HTML files to display to the user, runs client-side scripts, and initiates background network requests.
- **The Server (Node.js + Express):** The provider. It listens on a network port (`3001`), waits for client requests, processes logic (incrementing the counter and generating timestamps), and sends back responses.

---

## 4. Architecture & Request Flow Diagram

Here is what happens across the network when you use this application:

```text
+-----------------------------------------------------------------------------+
|                                 WEB BROWSER                                 |
|                                  (Client)                                   |
+-----------------------------------------------------------------------------+
       |                                                    ^
       | 1. User loads http://localhost:3001/               |
       |    GET / (HTML Request)                            | 2. Server returns
       v                                                    |    public/index.html
+-----------------------------------------------------------------------------+
|                            EXPRESS SERVER (Port 3001)                       |
|                                  (Backend)                                  |
+-----------------------------------------------------------------------------+

[ Browser displays the page. No student data is shown yet. ]

       |
       | 3. User clicks "Fetch Data" button
       |    Browser executes: fetch('/api/student')
       |    [Opens a NEW HTTP GET connection]
       v
+-----------------------------------------------------------------------------+
|                            EXPRESS SERVER (Port 3001)                       |
|  - Increments requestCount (e.g., 0 -> 1)                                   |
|  - Creates fresh timestamp (e.g., "5:30:15 PM")                             |
|  - Logs to terminal: "GET /api/student: request 1"                          |
|  - Bundles { name, branch, year, requestNumber, timestamp }                 |
+-----------------------------------------------------------------------------+
       |
       | 4. Server sends HTTP 200 OK with JSON response
       v
+-----------------------------------------------------------------------------+
|                                 WEB BROWSER                                 |
|  - Receives JSON payload                                                    |
|  - JavaScript parses: const data = await response.json()                    |
|  - Updates DOM table: Name: Saketh, Branch: CSE, Req: #1                    |
|  - Shows the student details table                                          |
+-----------------------------------------------------------------------------+

[ User clicks "Fetch Data" a second time... ]
--> A second connection is made to GET /api/student.
--> Server increments requestCount (1 -> 2) and generates a new timestamp.
--> Terminal logs: "GET /api/student: request 2".
--> Browser updates the table to show Request #2 and the new timestamp.
```

---

## 5. How to Run and Test This Practical

### Terminal Commands (PowerShell)
```powershell
# 1. Open the project folder
cd c:\Users\user\Downloads\HTML-Playground\HTML-Playground\Assignment-5

# 2. Install dependencies (runs once)
npm install

# 3. Start the server
node server.js
```

### In Your Browser
1. Navigate to **`http://localhost:3001`**.
2. Notice that the page loads cleanly, but **no student data is visible**.
3. Click the **Fetch Data** button.
   - The button disables briefly and shows a loading message.
   - The student information appears showing **Saketh**, **CSE**, **3rd Year**, **Request Number #1**, and a timestamp.
   - Look at your PowerShell terminal: you will see `GET /api/student: request 1`.
4. Click **Fetch Data** again.
   - The Request Number changes to **#2**, and the timestamp updates to the current second.
   - In the terminal, you will see `GET /api/student: request 2`.

---

## 6. Recommended Reading Order

To get the most out of your preparation, read the documentation files in this sequence:

1. **`START-HERE.md`** *(This file)*: High-level overview, mental models, and request flow.
2. **`EXPRESS-AND-FETCH.md`**: Theoretical explanation of Express, HTTP methods, JSON, and `fetch()`.
3. **`CODE-EXPLANATION.md`**: Detailed line-by-line breakdown of `server.js` and `public/index.html`.
4. **`HANDS-ON-EXERCISES.md`**: 6 quick coding exercises to test your understanding by making small edits.
5. **`VIVA-PREP.md`**: 18 common viva questions with concise, spoken answers.
6. **`GLOSSARY.md`**: Quick reference definitions for all key terminology.

---

## 7. Beginner 30-Minute Learning Plan

- **Minutes 0–5:** Run the server, open the browser, and click the button twice to see the live behavior and terminal output.
- **Minutes 5–15:** Read `EXPRESS-AND-FETCH.md` and `CODE-EXPLANATION.md` to see how the client JavaScript and server Express routes connect.
- **Minutes 15–22:** Try Exercises 1, 2, and 3 in `HANDS-ON-EXERCISES.md` (e.g. change the student name or add a new field).
- **Minutes 22–30:** Review the Q&A in `VIVA-PREP.md` so you can confidently answer questions during lab evaluation.
