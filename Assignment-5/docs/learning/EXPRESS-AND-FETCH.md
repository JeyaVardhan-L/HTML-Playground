# Assignment 5 — Express.js and the Browser Fetch API

This guide breaks down every fundamental networking and web concept used in Assignment 5 using simple, beginner-friendly explanations and concrete examples from our project.

---

## 1. What is a Server?

A **server** is simply a program running on a computer that listens for incoming connection requests over a network (such as the Internet or your local machine `localhost`) and sends back a response.

In our practical:
- The server is written in JavaScript and runs under **Node.js**.
- It listens on TCP port **`3001`**.
- It provides two things:
  1. The HTML user interface (`public/index.html`).
  2. The student data endpoint (`/api/student`).

---

## 2. What Does Express.js Do?

While Node.js provides a built-in `http` module, writing server routes and handling static files with vanilla Node.js requires dozens of lines of repetitive boilerplate code.

**Express.js** is a fast, minimalist web framework that simplifies this:
- **Routing:** Defining what happens when a user visits a specific URL (e.g. `app.get('/api/student', ...)`).
- **Static File Serving:** Express can automatically serve an entire folder of HTML, CSS, and JS files with one line: `app.use(express.static('public'))`.
- **JSON Serialization:** Express provides `res.json()`, which automatically converts JavaScript objects into properly formatted JSON text with the correct `Content-Type: application/json` header.

---

## 3. What are HTTP Requests and Responses?

HTTP (Hypertext Transfer Protocol) is the standard communication language of the web. It operates in a strict **request-response cycle**:
1. **The Request:** Sent by the client (browser) to ask the server for a resource or action.
2. **The Response:** Sent back by the server containing a status code (like `200 OK` or `404 Not Found`) and the requested content (HTML, JSON, images, etc.).

In our assignment, two different kinds of HTTP requests take place:
- **Initial Request:** The browser sends `GET http://localhost:3001/` to fetch `index.html`.
- **API Request:** When you click the button, the browser sends `GET http://localhost:3001/api/student` to fetch data.

---

## 4. What Does the GET Method Mean?

HTTP defines several request "methods" (verbs) indicating the desired action:
- **`GET`:** Used to retrieve or fetch data from a server without modifying anything on the server.
- **`POST`:** Used to submit new data to a server (e.g., submitting a form).
- **`PUT` / `PATCH`:** Used to update existing data.
- **`DELETE`:** Used to remove data.

In Assignment 5, we use `GET` because the client's sole intent is to read student information.

---

## 5. What is an API Endpoint?

An **API** (Application Programming Interface) allows two programs to talk to each other. An **endpoint** is a specific URL location on a server designated to handle certain requests.

In our project:
- Route: `/api/student`
- Method: `GET`
- Full URL: `http://localhost:3001/api/student`

When you visit this URL directly in your browser or through JavaScript `fetch()`, the server executes the callback function associated with `/api/student`.

---

## 6. What is JSON?

**JSON** stands for **JavaScript Object Notation**. It is a lightweight, human-readable data format used universally across the web to transfer data between servers and clients.

On the server, student information is stored as a native JavaScript object:
```javascript
const studentData = {
  name: "Alex Kumar",
  branch: "CSE",
  year: "3rd Year"
};
```

When `res.json(...)` is called, Express serializes this object into a JSON string sent across the network:
```json
{
  "name": "Alex Kumar",
  "branch": "CSE",
  "year": "3rd Year",
  "requestNumber": 1,
  "timestamp": "5:30:15 PM"
}
```

The browser receives this text string and deserializes it back into a JavaScript object it can work with.

---

## 7. What Does the Browser's `fetch()` API Do?

In modern browsers, `fetch()` is a built-in JavaScript function used to make asynchronous HTTP requests across the network without refreshing or reloading the webpage.

A basic fetch request looks like this:
```javascript
const response = await fetch("/api/student");
const data = await response.json();
```

Because network communication takes time (even on localhost), `fetch()` is **asynchronous**—it returns a JavaScript `Promise` that resolves once the server replies.

---

## 8. What Do `async/await`, `response.json()`, and `try/catch` Mean?

### `async` and `await`
- An **`async function`** is a function that contains asynchronous operations and automatically returns a Promise.
- The **`await`** keyword pauses the execution of the async function until the Promise settles (resolves or rejects), allowing asynchronous code to be written cleanly as if it were synchronous:
  ```javascript
  // Waits for the server to reply over the network
  const response = await fetch("/api/student");
  ```

### `response.json()`
- The raw `response` object returned by `fetch()` contains HTTP metadata (headers, status code).
- The actual body of the response arrives as a readable stream of text.
- Calling `await response.json()` parses that text into a usable JavaScript object.

### `try / catch / finally`
- **`try` Block:** Encloses code that might fail due to network disconnection, an offline server, or an invalid response.
- **`catch` Block:** Catches any error thrown in the `try` block, preventing the webpage from crashing and allowing you to show a user-friendly error message.
- **`finally` Block:** Always executes, regardless of whether the request succeeded or failed. This is the ideal place to re-enable the button and hide the loading spinner:
  ```javascript
  try {
    const response = await fetch("/api/student");
    const data = await response.json();
    // update DOM...
  } catch (err) {
    // show error to user...
  } finally {
    // always re-enable the button
    fetchBtn.disabled = false;
  }
  ```

---

## 9. Why a New Request is Made on Each Click

When you click **Fetch Data**, the event listener executes the `fetchStudentData()` function from scratch:

```javascript
fetchBtn.addEventListener("click", fetchStudentData);
```

Every click creates a new network socket connection from the browser to the Express server. The browser does NOT simply read from a cached variable in memory; it explicitly asks the server: *"Give me the latest student information right now."*

This is why clicking the button repeatedly produces separate logs on the server:
```text
GET /api/student: request 1
GET /api/student: request 2
GET /api/student: request 3
```

---

## 10. Why the Request Counter and Timestamp are Generated on the Server

If the browser counted the clicks or generated the time, the demonstration would only prove that client-side JavaScript works. 

By having the **Express server** calculate `requestCount += 1` and `new Date().toLocaleTimeString()`:
1. It proves that the request **actually traveled across the network** to the backend.
2. It proves that the server code executed and returned dynamic, freshly generated data.
3. If two different browsers connected to `http://localhost:3001`, Browser A would see request `#1`, and Browser B would see request `#2`. The state lives on the server.

---

## 11. Initial Page Request vs. Subsequent API Requests

Understanding the difference between these two types of requests is the single most important concept of this assignment:

| Property | Initial Page Request | API Request (`fetch`) |
| :--- | :--- | :--- |
| **Trigger** | Entering the URL in the address bar / hitting Refresh. | Clicking the **Fetch Data** button. |
| **URL** | `http://localhost:3001/` | `http://localhost:3001/api/student` |
| **Response Content** | HTML document (`index.html`) with CSS and JS. | Raw JSON data (`application/json`). |
| **Browser Action** | Clears the viewport and renders the whole page. | Keeps the page intact and updates only the table elements. |
| **User Experience** | Page flash / blank load screen. | Instant, seamless in-place UI update. |
