# Technical Glossary & Concepts Dictionary

A clear, beginner-friendly dictionary of web development, Node.js, Express, and React terms used throughout Assignment 4.

---

### API (Application Programming Interface)
A defined set of rules and protocols that allows two software programs to communicate. In Practical 1, our Express server provides an API route (`GET /api/student`) allowing the browser client to request student records.

---

### Asynchronous (`async` / `await`)
A programming pattern in JavaScript that allows long-running operations (like network requests or file reads) to execute in the background without freezing the execution of other code. `await` pauses execution of an `async` function until a Promise finishes.

---

### Client
The user-facing device or application (typically a web browser like Chrome or Firefox) that displays web pages and sends requests across a network to a server.

---

### Component
A self-contained, reusable building block of a user interface in React. Components encapsulate their own markup (JSX), styling, and behavior (state and event handlers). Examples: `<StateCounter />`, `<StudentCard />`.

---

### CORS (Cross-Origin Resource Sharing)
A browser security mechanism that restricts a web page on one domain or port from making HTTP requests to a different domain or port unless the server explicitly grants permission.

---

### DOM (Document Object Model)
The tree-like data structure created by the web browser representing the HTML elements on a page. JavaScript can interact with the DOM to read or change HTML elements, styles, and attributes.

---

### Effect (Side Effect)
Any operation performed by a component that affects something outside the component's immediate rendering scope—such as updating the browser tab title (`document.title`), fetching data from a server, or setting up a timer. In React function components, side effects are managed using `useEffect`.

---

### Endpoint
A specific URL path and HTTP method exposed by a server where a particular resource can be accessed. For example: `GET /api/student`.

---

### Event Handler
A JavaScript function designed to execute in response to a user action, such as clicking a button (`onClick`), typing into a text field (`onChange`), or submitting a form (`onSubmit`).

---

### Express.js
A minimalist, flexible web application framework for Node.js. It simplifies setting up HTTP servers, serving static files, and routing incoming requests to custom API handlers.

---

### Fetch API (`fetch()`)
A modern, built-in browser JavaScript function used to send asynchronous HTTP requests across the network to retrieve or submit data without reloading the entire web page.

---

### Hook
A special JavaScript function provided by React (prefixed with `use`, such as `useState`, `useRef`, `useEffect`) that allows function components to use state, lifecycle methods, and direct DOM references without writing class components.

---

### HTTP (Hypertext Transfer Protocol)
The foundational communication protocol used for transmitting data (HTML, JSON, images) across the World Wide Web between clients and servers.

---

### JSON (JavaScript Object Notation)
A lightweight, human-readable text format for storing and exchanging structured data. It looks identical to a standard JavaScript object literal with double-quoted keys. Example: `{"name": "Aarav Sharma", "rollNumber": "2024-WAF-001"}`.

---

### JSX (JavaScript XML)
A syntax extension for JavaScript that allows developers to write HTML-like markup directly inside JavaScript files. It is compiled by tools like Vite into native `React.createElement()` calls.

---

### Localhost
The standard hostname referring to your own computer (`127.0.0.1`). When running servers locally, `http://localhost:3000` refers to port 3000 on your local machine.

---

### Middleware
Functions in Express that execute during the lifecycle of an incoming HTTP request before reaching the final route handler. Middleware can log requests, serve static assets, or authenticate users.

---

### Port
A virtual communication gateway (identified by a 16-bit number, like 3000 or 5173) that operating systems use to distinguish between different network programs running on the same computer simultaneously.

---

### Props (Properties)
Arguments passed from a parent component down to a child component in React. Props are **read-only** (immutable) from the child's perspective and allow child components to render dynamic data.

---

### Render
The process in React where a component executes its function or `render()` method, evaluates its state and props, and returns a JSX description of what the user interface should look like.

---

### Request (HTTP Request)
A message sent from a client (the browser) to a server asking to retrieve information (`GET`), submit data (`POST`), or perform an action.

---

### Response (HTTP Response)
The message sent back from a server to a client after receiving a request. It contains a status code (e.g. `200 OK` or `404 Not Found`), headers, and optional body content (such as HTML or JSON).

---

### Server
A computer system or software application (such as our Node/Express app in `server.js`) that waits for incoming network requests from clients, processes them, and returns responses.

---

### SPA (Single Page Application)
A web application model where a single HTML document is loaded, and subsequent user interactions update parts of the page dynamically using JavaScript (DOM manipulation or React) without performing full-page browser reloads.

---

### State
Data managed internally within a React component that can change over time based on user interactions. When state changes (via `setState` or `setCount`), React automatically re-renders the component to reflect the new state.

---

### Virtual DOM
An in-memory, lightweight copy of the browser's real DOM maintained by React. When state changes, React compares the new Virtual DOM with the previous snapshot (diffing) and efficiently updates only the changed nodes in the actual DOM.

---

### Vite
A modern, fast frontend build tool and local development server for JavaScript and React applications. It uses native browser ES modules to achieve instant startup and near-instant Hot Module Replacement (HMR).
