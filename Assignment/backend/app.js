const express = require("express");
const booksRouter = require("./routes/books");

const app = express();

app.use(express.json());

app.use((req, res, next) => {
  console.log(`[${new Date().toISOString()}] ${req.method} ${req.url}`);
  next();
});

app.use("/api/books", booksRouter);

app.use((req, res) => {
  res.status(404).json({ success: false, message: "Route not found." });
});

app.use((err, req, res, next) => {
  console.error("Unhandled error:", err.message);
  res.status(500).json({ success: false, message: "Internal server error." });
});

const PORT = 4000;
app.listen(PORT, () => {
  console.log(`Book API server running on http://localhost:${PORT}`);
  console.log("Available routes:");
  console.log("  GET    /api/books");
  console.log("  PUT    /api/books/:id/author");
  console.log("  DELETE /api/books/expensive");
});
