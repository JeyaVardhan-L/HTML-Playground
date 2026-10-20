# Assignment 5 — Glossary of Web and Networking Terms

A handy reference defining key concepts used in Assignment 5 in straightforward, non-academic English.

---

### Client
The user-facing device or software (such as Google Chrome, Firefox, or Safari) that initiates network requests to retrieve resources and renders the interface for the user.

### Server
A computer or background software application (such as our Express app) that continuously listens on a network port for client requests, processes data, and sends back appropriate responses.

### Node.js
An open-source, cross-platform JavaScript runtime environment built on Google Chrome's V8 engine that allows developers to run JavaScript code outside of a web browser on the server operating system.

### Express.js
A lightweight, fast, and flexible backend web application framework for Node.js. It simplifies routing HTTP requests, serving static files, and building RESTful web APIs.

### HTTP (Hypertext Transfer Protocol)
The foundational communication protocol used across the World Wide Web. It governs how messages (requests and responses) are formatted and transmitted between clients and servers.

### GET Method
An HTTP request method used specifically to request or retrieve data from a specified resource on a server. GET requests are idempotent and should not alter the state of data on the server.

### Request
A message sent from the client to the server asking for a specific action or resource, including headers (metadata), a target URL, and an HTTP method.

### Response
A message sent from the server back to the client containing an HTTP status code (e.g. `200 OK`, `404 Not Found`), response headers, and the payload body (HTML, JSON, plain text, or binary).

### API (Application Programming Interface)
A defined set of rules, protocols, and tools that allows different software applications to communicate and exchange data with one another.

### Endpoint
A specific digital location or URL on a server (e.g., `http://localhost:3001/api/student`) where a client can send requests to interact with an API.

### JSON (JavaScript Object Notation)
A standardized, text-based data interchange format based on JavaScript object syntax. It is human-readable, lightweight, and supported natively by virtually all programming languages.

### Fetch API
A modern, built-in browser interface (`window.fetch()`) that allows JavaScript code in a webpage to execute asynchronous HTTP requests across the network without refreshing the page.

### Asynchronous
An execution model where tasks (such as network requests or disk reads) are started in the background without blocking the execution of subsequent code. The program continues to run, handling the result once the background task finishes.

### `async` / `await`
Special JavaScript syntax that makes working with asynchronous Promises simpler and more readable. Marking a function with `async` allows using `await` inside it to pause execution until a Promise resolves.

### Error Handling
The programming practice of anticipating, detecting, and gracefully managing runtime errors or network failures (using `try/catch` blocks) so the application does not crash and provides clear feedback to the user.

### Request Counter
A server-side integer variable that begins at zero and increments each time an incoming request hits an endpoint. In our project, it proves that each button click generated a distinct, counted request on the backend.

### Timestamp
A formatted string indicating the exact moment (date and time) a particular event occurred. Generating the timestamp on the server for each request proves the response was freshly computed at that instant.
