const { getMessage } = require('../models/messageModel');
function showMessage(req, res) {

    const data = getMessage();
    res.render('view', { message: data });
}
module.exports = { showMessage };