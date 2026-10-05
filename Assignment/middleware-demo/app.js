const express = require("express");

const app = express();

function middlewareOne(req, res, next) {
  console.log("Middleware 1: Request received. Logging the incoming request.");
  next();
}

function middlewareTwo(req, res, next) {
  console.log("Middleware 2: Checking if request method is allowed.");
  if (req.method !== "GET" && req.method !== "POST") {
    return res.status(405).json({ message: "Method not allowed." });
  }
  next();
}

function middlewareThree(req, res, next) {
  console.log("Middleware 3: Adding a timestamp to the request object.");
  req.requestTime = new Date().toISOString();
  next();
}

app.use(middlewareOne);
app.use(middlewareTwo);
app.use(middlewareThree);

app.get("/", (req, res) => {
  console.log("Route handler: Sending the response.");
  res.json({
    message: "Hello from the route handler!",
    requestReceivedAt: req.requestTime,
  });
});

app.get("/stop-early", middlewareOne, (req, res, next) => {
  console.log("STOP-EARLY middleware: This middleware does NOT call next().");
  res.json({ message: "Response sent from middleware. The route handler never ran." });
}, (req, res) => {
  console.log("This line will never be printed because next() was not called above.");
  res.json({ message: "You will never see this." });
});

app.use((err, req, res, next) => {
  console.error("Error-handling middleware caught:", err.message);
  res.status(500).json({ error: err.message });
});

const PORT = 4001;
app.listen(PORT, () => {
  console.log(`Middleware demo server running on http://localhost:${PORT}`);
  console.log("Try: GET http://localhost:4001/");
  console.log("Try: GET http://localhost:4001/stop-early");
});
