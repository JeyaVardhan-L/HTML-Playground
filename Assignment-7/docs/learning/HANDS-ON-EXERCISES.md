# Assignment 7 — Hands-On Exercises: Step-by-Step Practical Tasks

These eight hands-on exercises will test and deepen your understanding of MongoDB cursor manipulation, BSON types, safe deletions, regular expressions, and atomic operations.

---

## Exercise 1: Change Top 3 Scorers to Top 5 Scorers
- **File to Edit:** `scripts/top-three.js`
- **Intended Change:** Modify the query to display the top 5 students instead of top 3.
- **Hint:** Change `.limit(3)` to `.limit(5)`:
  ```javascript
  .limit(5)
  ```
- **Expected Result:** Running `npm run top-three` displays Meera (94), Pooja (91), Aarav (88), Manish (78), and Vikram (72).

---

## Exercise 2: Change the Tie-Breaker to Student Name
- **File to Edit:** `scripts/top-three.js`
- **Intended Change:** Change the secondary sort tie-breaker from `rollNo: 1` to `name: 1` (alphabetical by name).
- **Hint:** Update the `.sort()` object:
  ```javascript
  .sort({ marks: -1, name: 1 })
  ```
- **Expected Result:** If two students have identical marks, they will now be ordered alphabetically by name.

---

## Exercise 3: Pass a Dynamic Student ID to `find-by-id.js` via CLI
- **File to Run:** PowerShell
- **Intended Change:** Instead of querying the default Aarav Sharma ID, look up Meera Nair (`65f1b2b2b2b2b2b2b2b2b102`) from the command line.
- **Command:**
  ```powershell
  node scripts/find-by-id.js 65f1b2b2b2b2b2b2b2b2b102
  ```
- **Expected Result:** The script outputs Meera Nair's record and demonstrates that `new ObjectId("65f1b2b2b2b2b2b2b2b2b102")` successfully retrieves her document.

---

## Exercise 4: Test Safe Deletion with Non-Interactive Confirmation
- **File to Run:** PowerShell
- **Intended Change:** Run `delete-below-40.js` with the `--confirm` bypass flag.
- **Command:**
  ```powershell
  node scripts/delete-below-40.js --confirm
  ```
- **Expected Result:** The script proceeds without pausing for interactive confirmation, deletes 2 students (Rohan Varma and Suresh Iyer), and displays remaining student count (6).
- **Cleanup / Restore:** Run `npm run seed` to restore all records.

---

## Exercise 5: Search for Names Ending with 'a' Using `$regex`
- **File to Edit:** `scripts/names-starting-m.js`
- **Intended Change:** Change the regex from `^M` (starts with M) to `a$` (ends with the letter 'a', case-insensitive).
- **Hint:** Change the query object:
  ```javascript
  const query = {
    name: {
      $regex: "a$",
      $options: "i"
    }
  };
  ```
- **Expected Result:** Running `node scripts/names-starting-m.js` will match names ending in 'a': `Aarav Sharma`, `Meera Nair`, `Pooja Reddy`, and `Neha Patel`.

---

## Exercise 6: Add a New Book to the Library Management System
- **File to Edit:** `scripts/seed.js`
- **Intended Change:** Add a 5th book: `"The Pragmatic Programmer"` by `"David Thomas and Andrew Hunt"` with 5 copies.
- **Hint:** Add an object to the `books` array in `seed.js`:
  ```javascript
  {
    _id: new ObjectId("65f1c3c3c3c3c3c3c3c3c105"),
    title: "The Pragmatic Programmer",
    author: "David Thomas and Andrew Hunt",
    copies: 5
  }
  ```
- **Expected Result:** Run `npm run seed` then `node scripts/library-management.js list`. The new book appears in the catalog with 5 copies.

---

## Exercise 7: Test Zero-Copy Rejection in Library System
- **File to Run:** PowerShell
- **Intended Change:** Attempt to issue `"JavaScript: The Definitive Guide"`, which was seeded with 0 copies.
- **Command:**
  ```powershell
  node scripts/library-management.js issue "JavaScript: The Definitive Guide"
  ```
- **Expected Result:** The program prints:
  `✗ UNAVAILABLE: "JavaScript: The Definitive Guide" is currently out of stock (0 copies available). Cannot issue.`
  And confirms that the database was not modified.

---

## Exercise 8: Test Issue and Return Flow via CLI
- **File to Run:** PowerShell
- **Intended Change:** Issue one copy of `"Clean Code"` (starting with 3 copies), verify count is 2, then return it and verify count is 3.
- **Commands:**
  ```powershell
  node scripts/library-management.js issue "Clean Code"
  node scripts/library-management.js list
  node scripts/library-management.js return "Clean Code"
  node scripts/library-management.js list
  ```
- **Expected Result:** You will observe `copies` decrement to 2 on issue, and increment back to 3 on return.
