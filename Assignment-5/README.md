# Web Application Frameworks (WAF) — Lab Assignment 5
## Fetching Data with a New Connection Using Express.js

**Subject:** Web Application Frameworks (WAF) Lab  
**Assignment:** Lab Assignment 5 — Fetching the data with a new connection using Express js  
**Technologies:** Node.js, Express.js (v4), Vanilla JavaScript (Browser Fetch API), HTML5, CSS3  
**Port:** `3001`  
**Student:** Student Name · Department of Computer Science & Engineering (CSE), 3rd Year  

---

## 1. Assignment Purpose

The goal of this practical is to demonstrate how a client (web browser) communicates with a backend server (Node.js + Express) across separate, distinct HTTP connections:

1. **Initial Connection (Page Delivery):** The browser connects to `http://localhost:3001/` to download `index.html`. No student data is transferred or displayed yet.
2. **On-Demand Connections (Data Retrieval):** Each time the user clicks **Fetch Data**, the browser opens a **brand new HTTP GET request** to `/api/student`.
3. **Dynamic Server Processing:** The Express server receives the request, increments its internal counter (`requestCount`), captures the current server-side timestamp, logs the request count to the terminal, and replies with a JSON payload.
4. **Asynchronous DOM Update:** The client receives the JSON response, parses it, and dynamically renders the student details, request number, and timestamp without reloading the page.

---

## 2. Technologies Used

- **Node.js:** Server-side JavaScript runtime environment.
- **Express.js:** Minimalist web application framework for routing and serving static assets.
- **Fetch API:** Native browser API (`window.fetch`) for making asynchronous HTTP requests using `async` / `await`.
- **Vanilla HTML5 & CSS3:** Lightweight, accessible markup styled with a clean college-lab design (no third-party UI libraries, external fonts, or build tools).

---

## 3. Directory Structure

```text
Assignment-5/
├── README.md                      ← Overview, setup commands, expected behavior & checklist
├── package.json                   ← Project metadata, dependencies (express), and start script
├── server.js                      ← Express server on port 3001 with request counter & logging
├── public/
│   └── index.html                 ← Minimalist HTML UI with Fetch Data button & async script
└── docs/
    └── learning/
        ├── START-HERE.md          ← Orientation, architecture diagrams & study roadmap
        ├── EXPRESS-AND-FETCH.md   ← Core concepts: Express, HTTP GET, JSON & Fetch API
        ├── CODE-EXPLANATION.md    ← Line-by-line breakdown of server.js and index.html
        ├── VIVA-PREP.md           ← 18 high-yield viva questions with spoken model answers
        ├── HANDS-ON-EXERCISES.md  ← 6 beginner coding exercises with hints and solutions
        └── GLOSSARY.md            ← Definitions of key networking and web terms
```

---

## 4. Prerequisites

Before running this project, ensure **Node.js** (v18 or higher recommended) and **npm** are installed:

```powershell
node -v
npm -v
```

---

## 5. Installation & Startup (PowerShell)

Open Windows PowerShell and run the following commands:

### Step 1: Navigate to the Assignment 5 directory
```powershell
cd c:\Users\user\Downloads\HTML-Playground\HTML-Playground\Assignment-5
```

### Step 2: Install dependencies
```powershell
npm install
```

### Step 3: Start the Express server
```powershell
npm start
```
*(Alternatively, run: `node server.js`)*

The terminal will display:
```text
==================================================
Express server running on http://localhost:3001
API endpoint: http://localhost:3001/api/student
Ready to receive client requests...
==================================================
```

---

## 6. Accessing the Application

1. Open your web browser (Chrome, Edge, or Firefox).
2. Visit: **`http://localhost:3001`**

---

## 7. Expected Demonstration Behavior

| State | Browser UI | Terminal Output |
| :--- | :--- | :--- |
| **Before 1st Click** | Shows heading, explanation, and enabled **Fetch Data** button. The student details area is **hidden**. | Displays startup banner only. No request logs. |
| **After 1st Click** | Briefly shows loading indicator. Table appears showing:<br>• **Student Name:** Student Name<br>• **Branch:** CSE<br>• **Year:** 3rd Year<br>• **Request Number:** `#1`<br>• **Fetch Timestamp:** *(current time)* | `GET /api/student: request 1` |
| **After 2nd Click** | Request number increments to **`#2`**. Timestamp updates to the exact new moment of the second request. | `GET /api/student: request 2` |
| **Subsequent Clicks** | Request number increments continuously (`#3`, `#4`, etc.) with fresh timestamps on every click. | Logs `GET /api/student: request 3`, `request 4`, etc. |

---

## 8. Verification Checklist

- [x] Server starts cleanly on port `3001`.
- [x] `http://localhost:3001` serves `public/index.html`.
- [x] Initial page load does NOT automatically fetch student data.
- [x] Clicking **Fetch Data** triggers a real network request to `/api/student`.
- [x] Server terminal logs each request with incrementing count (`request 1`, `request 2`).
- [x] Response contains student fields (`name`, `branch`, `year`), `requestNumber`, and dynamic `timestamp`.
- [x] Error handling is present (displays helpful message if the server is stopped).
- [x] Button disables during pending request and re-enables in `finally`.
