// app.js

const express = require('express');
const app = express();

// Tell Express to use EJS as our View Engine
app.set('view engine', 'ejs');

// Import the Controller
const { showMessage } = require('./controllers/messageController');

// When the user goes to the home page ('/'), run the showMessage function
app.get('/', showMessage);

// Start the server on port 3000
app.listen(3000, () => {
    console.log('Server is running on http://localhost:3000');
});