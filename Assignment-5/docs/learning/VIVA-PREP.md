# Assignment 5 — Viva Preparation: High-Yield Questions & Spoken Answers

This document contains 18 likely viva questions for Assignment 5. The answers are written in clear, concise language that you can comfortably speak aloud during your laboratory assessment.

---

### Q1: What is the main objective of this practical?
**Answer:**  
"The objective is to demonstrate client-server communication using Express.js and the browser Fetch API. It shows that clicking 'Fetch Data' initiates a new HTTP connection to the server each time, and the server returns dynamic JSON data with an incremented request counter and fresh timestamp."

---

### Q2: What is the difference between Node.js and Express.js?
**Answer:**  
"Node.js is a runtime environment that allows JavaScript to run on the server side outside of a web browser. Express.js is a minimal web application framework that runs on top of Node.js to simplify routing, handling HTTP requests, and serving static files."

---

### Q3: What is the difference between a client and a server?
**Answer:**  
"A client is the program requesting resources—in our case, the web browser displaying the HTML interface. A server is the program that listens on a network port, processes client requests, and sends back appropriate responses."

---

### Q4: Why are two separate types of HTTP requests used in this practical?
**Answer:**  
"The first request is an initial HTTP GET request to `http://localhost:3001/` which downloads the static `index.html` page. The subsequent requests are asynchronous API requests made via `fetch('/api/student')` when the user clicks the button. This updates the data on the page without reloading it."

---

### Q5: What is an API endpoint?
**Answer:**  
"An API endpoint is a specific URL location on a server that handles incoming requests for a specific resource or action. In our project, `/api/student` is the endpoint that returns student details in JSON format."

---

### Q6: Why do we use the HTTP GET method here instead of POST?
**Answer:**  
"We use GET because our intention is purely to retrieve and read data from the server without submitting new records or modifying database records. GET is the standard HTTP method for read operations."

---

### Q7: What is JSON and why do we use it here?
**Answer:**  
"JSON stands for JavaScript Object Notation. It is a lightweight, text-based data exchange format that is language-independent and easily parsed by both servers and browsers. Our Express server converts JavaScript objects to JSON using `res.json()`, and the browser parses it with `response.json()`."

---

### Q8: What does the browser `fetch()` API do?
**Answer:**  
"The `fetch()` API is a native browser function used to make asynchronous network requests. It returns a JavaScript Promise that resolves into the server's response object when the request completes, allowing web pages to update dynamically without a full page refresh."

---

### Q9: Why is `async` and `await` used with `fetch()`?
**Answer:**  
"`fetch()` is an asynchronous operation because network requests take time to complete. Using `async` and `await` allows us to write asynchronous code that reads like normal synchronous code, pausing execution until the promise resolves instead of using nested `.then()` callback chains."

---

### Q10: Why do we need `try/catch` and `finally` blocks around the fetch call?
**Answer:**  
"Network requests can fail due to server disconnection, incorrect URLs, or network dropouts. The `try/catch` block catches network errors gracefully and displays a message to the user instead of throwing an unhandled exception. The `finally` block ensures that the button is always re-enabled and the loading indicator is hidden regardless of success or failure."

---

### Q11: Why is the request counter maintained on the server instead of the browser?
**Answer:**  
"Maintaining `requestCount` on the server proves that each click actually reached the backend over the network. If the counter were in the browser, it would only count local button clicks. Having it on the server proves that a real, distinct request was received and processed by Express."

---

### Q12: Why is the timestamp generated on the server?
**Answer:**  
"Generating the timestamp on the server using `new Date().toLocaleTimeString()` ensures that the response is dynamic and proves the exact time the server processed that specific request, rather than returning a pre-generated, static JSON file."

---

### Q13: What does `app.use(express.static(path.join(__dirname, "public")))` do?
**Answer:**  
"This is built-in Express middleware that tells the server to automatically serve all static files located inside the `public` directory, such as `index.html`, whenever a client requests them."

---

### Q14: How does the server terminal reflect the client's requests?
**Answer:**  
"Inside the `GET /api/student` route handler, we have `console.log('GET /api/student: request ' + requestCount)`. Every time a user clicks 'Fetch Data', this line prints to the server terminal, showing `request 1`, `request 2`, and so on."

---

### Q15: What happens if you click 'Fetch Data' while the Express server is stopped?
**Answer:**  
"The browser cannot establish a TCP connection to port 3001, so `fetch()` rejects with a TypeError ('Failed to fetch'). The `catch` block catches this error and displays an error message informing the user to ensure the server is running on port 3001."

---

### Q16: What does `response.ok` check in the fetch logic?
**Answer:**  
"`response.ok` is a boolean property of the Response object that is `true` if the HTTP status code is in the 200–299 range (successful). If the server returns a 404 or 500 status code, `fetch()` does not automatically throw an error, so we check `if (!response.ok)` and throw our own error."

---

### Q17: On which port does the server listen, and how is port conflict handled?
**Answer:**  
"The server listens on port `3001`. We attach an error listener `server.on('error', ...)` that checks if `err.code === 'EADDRINUSE'`. If another process is already using port 3001, it prints a clear error message explaining the conflict rather than crashing silently."

---

### Q18: What are the exact steps to start and verify this practical from scratch?
**Answer:**  
"1. Open PowerShell and navigate to `Assignment-5/`.  
2. Run `npm install` to install Express.  
3. Run `node server.js` to start the server on port 3001.  
4. Open a web browser to `http://localhost:3001`.  
5. Click 'Fetch Data' twice and verify that the request number increments from 1 to 2 in both the browser table and the server terminal."
