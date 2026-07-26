const express = require('express');
const app = express();
app.set('view engine', 'ejs');
const { showMessage } = require('./controllers/messageController');
app.get('/', showMessage);
app.listen(3000, () => {
    console.log('Server is running on http://localhost:3000');
});