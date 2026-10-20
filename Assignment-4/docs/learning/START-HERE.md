# Start Here: Assignment 4 Learning Roadmap

Welcome to the beginner's learning guide for **Web Application Frameworks (WAF) Lab Assignment 4**!

In **Assignment 2**, we mastered HTML layout and CSS styling. In **Assignment 3**, we brought pages to life using core JavaScript DOM methods and events.

Now, in **Assignment 4**, we take the next major leap in web development: **Full-Stack Architecture and Component-Based Frontends**.

---

## 1. How the Technologies Fit Together

Modern web development divides responsibility into two primary domains: the **Client (Frontend)** and the **Server (Backend)**.

```text
+-------------------------------------------------------------------------------------------------+
|                                    FULL-STACK WEB ARCHITECTURE                                  |
|                                                                                                 |
|   CLIENT / BROWSER (Port 3000 or 5173)                 SERVER / NODE.JS RUNTIME (Port 3000)     |
|   +---------------------------------------+             +------------------------------------+  |
|   | 1. HTML / JSX (Structure & Markup)    |             | 1. Node.js (JavaScript Runtime)    |  |
|   | 2. CSS (Styling & Design Tokens)      |             | 2. Express.js (HTTP Web Server)    |  |
|   | 3. React (Component UI Library)       |             | 3. REST API Routes (/api/student)  |  |
|   | 4. Fetch API (Network Requests)       |             | 4. Data Storage (JSON / Database)  |  |
|   +---------------------------------------+             +------------------------------------+  |
|                       |                                                   ^                     |
|                       |  HTTP Request (GET /api/student)                  |                     |
|                       +---------------------------------------------------+                     |
|                       |                                                                         |
|                       |  HTTP Response (200 OK + JSON Data)                                     |
|                       <---------------------------------------------------+                     |
+-------------------------------------------------------------------------------------------------+
```

### The Roles in Plain English:
1. **Node.js**: Allows us to run JavaScript *outside* the browser, directly on our computer operating system.
2. **Express.js**: A lightweight Node.js framework that listens on a port (like `3000`), receives HTTP requests from browsers, and sends back files or JSON data.
3. **React**: A frontend library created by Meta that allows us to build user interfaces out of reusable, independent Lego-like blocks called **Components**.
4. **Fetch API**: The browser's built-in mechanism for requesting data from a server behind the scenes without reloading the page.

---

## 2. What is a Server? What is a Component?

### What is a Server?
Think of a **Server** like a waiter in a restaurant:
- You (the customer/client) look at the menu and place an order (the **Request**).
- The waiter walks to the kitchen, gets your food, and brings it to your table (the **Response**).
- In our project, Express is the server. When you visit `http://localhost:3000`, Express serves `public/index.html`. When you click "Fetch Data", Express serves the student record JSON.

### What is a Component?
In traditional HTML, a webpage is one massive file. In **React**, we slice the interface into small, self-contained pieces called **Components**:
- A component is a JavaScript function or class that returns a piece of user interface (written in JSX).
- Components can manage their own internal state (like a counter) and can be reused as many times as you want.
- In our project, `<StateCounter />`, `<ClassStudent />`, and `<StudentCard />` are all individual components.

---

## 3. Flow Diagram: The Practical 1 Request & Response Lifecycle

Here is what happens when you click **"Fetch Data"** in Practical 1:

```text
[User clicks "Fetch Data" button in browser]
                     |
                     v
1. fetchStudentData() async function is triggered
                     |
                     v
2. Browser sends HTTP GET request over network:
   --> GET http://localhost:3000/api/student
                     |
                     v
3. Express Server (server.js) intercepts request on port 3000:
   --> console.log("[EXPRESS SERVER ...] Received GET request for /api/student")
   --> Formats studentData as JSON
   --> Sends HTTP 200 OK response with JSON header
                     |
                     v
4. Browser receives raw JSON text stream:
   --> const data = await response.json();
                     |
                     v
5. Browser DOM updates:
   --> studentName.textContent = data.name;
   --> studentRoll.textContent = data.rollNo;
   --> studentContainer.style.display = "block";
   (Student record appears green and populated on the screen!)
```

Notice that the initial HTML page load and this later data-fetch are **two completely separate requests**. The page never reloads!

---

## 4. The Six Practicals Summary

| Practical | Folder / File | What It Demonstrates |
| :--- | :--- | :--- |
| **Practical 1** | `express-fetch/` | Express.js backend serving HTML, custom `GET /api/student` JSON endpoint, terminal logging, and asynchronous client-side `fetch()` with `async/await` and `try/catch`. |
| **Practical 2** | `react-practicals/src/components/StateCounter.jsx` | React State management using the `useState(0)` hook to increment, decrement, and reset a reactive counter that re-renders instantly. |
| **Practical 3** | `react-practicals/src/components/ClassStudent.jsx` | Legacy React Class Component syntax extending `React.Component`, constructor state, and the mandatory `render()` method. |
| **Practical 4** | `react-practicals/src/components/StudentProps.jsx` | Passing read-only `props` from a Parent component down to reusable `<StudentCard />` Child components mapped over a data array. |
| **Practical 5** | `react-practicals/src/components/HooksDemo.jsx` | Demonstrating three essential hooks in one app: `useState` (state values), `useRef` (DOM node focusing), and `useEffect` (synchronizing the browser tab title). |
| **Practical 6** | `react-practicals/src/components/FunctionStudent.jsx` | Modern standard React Function Component returning readable JSX to describe the student record UI. |

---

## 5. Recommended Reading Order

Work through the learning documents in this order:

```text
1. START-HERE.md            <-- You are here
       |
       v
2. EXPRESS-AND-FETCH.md     <-- Understand servers, ports, HTTP GET, JSON, and browser fetch()
       |
       v
3. REACT-FROM-ZERO.md       <-- Master components, JSX, props, state, and the 3 hooks
       |
       v
4. CODE-EXPLANATION.md      <-- Line-by-line tour of all 6 practicals and interaction traces
       |
       v
5. HANDS-ON-EXERCISES.md    <-- 10 small coding exercises to test your understanding
       |
       v
6. VIVA-PREP.md             <-- 26 high-yield exam questions with spoken model answers
       |
       v
7. GLOSSARY.md              <-- Full-stack terminology cheat sheet
```

---

## 6. How to Run the Assignment

You will run two separate commands in two separate terminal windows:

### Terminal 1: Practical 1 (Express Server)
```powershell
cd c:\Users\user\Downloads\HTML-Playground\HTML-Playground\Assignment-4\express-fetch
npm start
```
Open your browser to: **`http://localhost:3000`**

### Terminal 2: Practicals 2–6 (React Laboratory)
```powershell
cd c:\Users\user\Downloads\HTML-Playground\HTML-Playground\Assignment-4\react-practicals
npm run dev
```
Open your browser to: **`http://localhost:5173`**

Let's dive into backend fundamentals with [EXPRESS-AND-FETCH.md](EXPRESS-AND-FETCH.md)!
