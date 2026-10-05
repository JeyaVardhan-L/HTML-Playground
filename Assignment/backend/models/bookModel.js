let books = [
  { id: 1, title: "Clean Code", author: "Robert C. Martin", price: 150 },
  { id: 2, title: "The Pragmatic Programmer", author: "Andy Hunt", price: 175 },
  { id: 3, title: "JavaScript: The Good Parts", author: "Douglas Crockford", price: 120 },
  { id: 4, title: "You Don't Know JS", author: "Kyle Simpson", price: 200 },
  { id: 5, title: "Design Patterns", author: "Gang of Four", price: 210 },
  { id: 6, title: "Introduction to Algorithms", author: "Cormen et al.", price: 195 },
  { id: 7, title: "Node.js in Action", author: "Mike Cantelon", price: 185 },
  { id: 8, title: "Learning React", author: "Alex Banks", price: 160 },
];

function getAllBooks() {
  return books;
}

function findBookById(id) {
  return books.find((b) => b.id === id);
}

function updateBookAuthor(id, newAuthor) {
  const book = findBookById(id);
  if (!book) return null;
  book.author = newAuthor;
  return book;
}

function deleteExpensiveBooks() {
  const removed = books.filter((b) => b.price > 190);
  books = books.filter((b) => b.price <= 190);
  return removed;
}

module.exports = { getAllBooks, findBookById, updateBookAuthor, deleteExpensiveBooks };
