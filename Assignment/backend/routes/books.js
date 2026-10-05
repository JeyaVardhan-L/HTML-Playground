const express = require("express");
const router = express.Router();
const bookController = require("../controllers/bookController");

router.get("/", bookController.getAllBooks);
router.put("/:id/author", bookController.updateAuthor);
router.delete("/expensive", bookController.deleteExpensive);

module.exports = router;
