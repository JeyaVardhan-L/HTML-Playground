/**
 * Assignment 7 — Requirement 10
 * Library Management Program using MongoDB "books" collection
 *
 * Demonstrates:
 * 1. Managing a "books" collection: { title, author, copies }.
 * 2. Atomic updates using MongoDB operators:
 *    - Issue: findOneAndUpdate({ title, copies: { $gt: 0 } }, { $inc: { copies: -1 } })
 *      -> Guaranteed never to decrement below 0, even under concurrent access!
 *    - Return: findOneAndUpdate({ title }, { $inc: { copies: 1 } })
 * 3. Handling edge cases:
 *    - Non-existent books (clean error message)
 *    - Zero-copy books (clear message: "No copies currently available")
 * 4. Dual operation modes:
 *    - Interactive terminal menu (node scripts/library-management.js)
 *    - Non-interactive CLI commands for scripting and quick demonstration:
 *        node scripts/library-management.js list
 *        node scripts/library-management.js issue "<title>"
 *        node scripts/library-management.js return "<title>"
 */

const { MongoClient, ObjectId } = require("mongodb");
const readline = require("readline");

const MONGODB_URI = process.env.MONGODB_URI || "mongodb://127.0.0.1:27017/waf_assignment_7";
const DB_NAME = "waf_assignment_7";

// Sample seed books
const INITIAL_BOOKS = [
  {
    _id: new ObjectId("65f1c3c3c3c3c3c3c3c3c101"),
    title: "Clean Code",
    author: "Robert C. Martin",
    copies: 3
  },
  {
    _id: new ObjectId("65f1c3c3c3c3c3c3c3c3c102"),
    title: "Design Patterns",
    author: "Erich Gamma et al.",
    copies: 2
  },
  {
    _id: new ObjectId("65f1c3c3c3c3c3c3c3c3c103"),
    title: "JavaScript: The Definitive Guide",
    author: "David Flanagan",
    copies: 0 // Explicit 0 copies for edge-case demonstration
  },
  {
    _id: new ObjectId("65f1c3c3c3c3c3c3c3c3c104"),
    title: "Database System Concepts",
    author: "Abraham Silberschatz",
    copies: 4
  }
];

/**
 * Ensure sample books exist in database
 */
async function ensureBooksSeeded(booksCol) {
  const count = await booksCol.countDocuments();
  if (count === 0) {
    for (const b of INITIAL_BOOKS) {
      await booksCol.updateOne({ title: b.title }, { $set: b }, { upsert: true });
    }
  }
}

/**
 * 1. List All Books
 */
async function listBooks(booksCol) {
  const books = await booksCol.find({}).project({ _id: 0, title: 1, author: 1, copies: 1 }).sort({ title: 1 }).toArray();
  console.log("\n======================== Current Library Catalog ========================");
  if (books.length === 0) {
    console.log("No books currently in catalog.");
  } else {
    console.table(books);
  }
  console.log("=========================================================================\n");
  return books;
}

/**
 * 2. Issue a Book (Atomic decrement with condition copies > 0)
 */
async function issueBook(booksCol, title) {
  if (!title || title.trim() === "") {
    console.log("[ERROR] Please provide a valid book title.");
    return null;
  }

  const queryTitle = new RegExp(`^${title.trim()}$`, "i");

  // Atomic find and update with condition: copies > 0
  const result = await booksCol.findOneAndUpdate(
    { title: queryTitle, copies: { $gt: 0 } },
    { $inc: { copies: -1 } },
    { returnDocument: "after" }
  );

  if (result) {
    console.log(`\n✓ SUCCESS: Issued "${result.title}". Copies remaining: ${result.copies}\n`);
    return result;
  }

  // If update didn't match, check why: does the book exist with 0 copies or not at all?
  const existing = await booksCol.findOne({ title: queryTitle });
  if (!existing) {
    console.log(`\n✗ ERROR: Book "${title}" was not found in the library catalog.\n`);
  } else {
    console.log(`\n✗ UNAVAILABLE: "${existing.title}" is currently out of stock (0 copies available). Cannot issue.\n`);
  }
  return null;
}

/**
 * 3. Return a Book (Atomic increment)
 */
async function returnBook(booksCol, title) {
  if (!title || title.trim() === "") {
    console.log("[ERROR] Please provide a valid book title.");
    return null;
  }

  const queryTitle = new RegExp(`^${title.trim()}$`, "i");

  const result = await booksCol.findOneAndUpdate(
    { title: queryTitle },
    { $inc: { copies: 1 } },
    { returnDocument: "after" }
  );

  if (result) {
    console.log(`\n✓ SUCCESS: Returned "${result.title}". Total copies now available: ${result.copies}\n`);
    return result;
  } else {
    console.log(`\n✗ ERROR: Book "${title}" does not exist in our catalog.\n`);
    return null;
  }
}

/**
 * Interactive Terminal Menu Loop
 */
function promptUser(rl, question) {
  return new Promise(resolve => rl.question(question, resolve));
}

async function runInteractiveMenu(booksCol) {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });

  let running = true;

  console.log("================================================================================");
  console.log("Requirement 10: Terminal Library Management System (MongoDB)");
  console.log("================================================================================");

  while (running) {
    console.log("Menu Options:");
    console.log("  1. List all books");
    console.log("  2. Issue a book");
    console.log("  3. Return a book");
    console.log("  4. Exit");

    const choice = (await promptUser(rl, "\nEnter choice (1-4): ")).trim();

    switch (choice) {
      case "1":
        await listBooks(booksCol);
        break;
      case "2": {
        const title = await promptUser(rl, "Enter book title to issue: ");
        await issueBook(booksCol, title);
        break;
      }
      case "3": {
        const title = await promptUser(rl, "Enter book title to return: ");
        await returnBook(booksCol, title);
        break;
      }
      case "4":
      case "exit":
      case "quit":
        console.log("\nExiting library management program. Goodbye!");
        running = false;
        break;
      default:
        console.log("\n[INVALID CHOICE] Please enter a number between 1 and 4.\n");
    }
  }

  rl.close();
}

/**
 * Main Entry Point supporting both CLI flags and interactive menu
 */
async function main() {
  const client = new MongoClient(MONGODB_URI, { serverSelectionTimeoutMS: 3000 });

  try {
    await client.connect();
    const db = client.db(DB_NAME);
    const booksCol = db.collection("books");

    await ensureBooksSeeded(booksCol);

    const args = process.argv.slice(2);
    const command = args[0] ? args[0].toLowerCase() : null;

    if (command === "list") {
      await listBooks(booksCol);
    } else if (command === "issue") {
      const title = args.slice(1).join(" ") || "Clean Code";
      await issueBook(booksCol, title);
    } else if (command === "return") {
      const title = args.slice(1).join(" ") || "Clean Code";
      await returnBook(booksCol, title);
    } else {
      // Default: Interactive Menu
      await runInteractiveMenu(booksCol);
    }

  } catch (err) {
    console.error("\n[LIBRARY ERROR]", err.message);
    if (err.message.includes("ECONNREFUSED") || err.name === "MongoServerSelectionError") {
      console.error("\nCould not connect to MongoDB. Please ensure your MongoDB Community Server is running.");
      console.error("Default connection URI: mongodb://127.0.0.1:27017/waf_assignment_7");
      console.error("To start MongoDB on Windows: net start MongoDB (or run mongod.exe)");
    }
    process.exitCode = 1;
  } finally {
    await client.close();
  }
}

if (require.main === module) {
  main();
}

module.exports = { listBooks, issueBook, returnBook };
