exports.push = function (review) {
    var mysql = require('mysql');
    var date = require('node-datetime');
    var connection = mysql.createConnection({
        host: 'localhost',
        user: 'root',
        password: 'apmsetup',
        port: 3306,
        database: 'review'
    });

    var formatted = date.create().format('Y-m-d H:M:S');
    var data = [review[0], review[1], formatted];

    console.log(data);

    connection.query('INSERT INTO test (review, star, datetime) VALUES (?, ?, ?)', [review[0], review[1], formatted], function (err, res) {
        if (err) throw err;
    });
};