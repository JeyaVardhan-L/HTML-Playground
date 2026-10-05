const bookModel = require("../models/bookModel");

function getAllBooks(req, res) {
  const books = bookModel.getAllBooks();
  res.status(200).json({ success: true, count: books.length, data: books });
}

function updateAuthor(req, res) {
  const id = parseInt(req.params.id, 10);
  const { author } = req.body;

  if (!author || typeof author !== "string" || author.trim() === "") {
    return res.status(400).json({ success: false, message: "Author field is required and must be a non-empty string." });
  }

  const updated = bookModel.updateBookAuthor(id, author.trim());

  if (!updated) {
    return res.status(404).json({ success: false, message: `Book with id ${id} not found.` });
  }

  res.status(200).json({ success: true, message: "Author updated successfully.", data: updated });
}

function deleteExpensive(req, res) {
  const removed = bookModel.deleteExpensiveBooks();

  if (removed.length === 0) {
    return res.status(200).json({ success: true, message: "No books with price greater than 190 were found.", deletedCount: 0, deletedBooks: [] });
  }

  res.status(200).json({
    success: true,
    message: `${removed.length} book(s) with price > 190 deleted.`,
    deletedCount: removed.length,
    deletedBooks: removed,
  });
}

module.exports = { getAllBooks, updateAuthor, deleteExpensive };
