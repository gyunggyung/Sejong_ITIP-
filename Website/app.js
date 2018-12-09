const express = require('express');
var bodyParser = require('body-parser');
var python = require('./public/js/python');
var review = require('./public/js/review');

const app = express();

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended:true}));

app.use(express.static(__dirname+'/public'));
//app.use('/ajax', './js/ajax.js');
app.get('/', function (req, res) {
    res.sendFile(__dirname+"/index.html");
});

app.get('/test', (req, res) => res.send('hello'));

app.post('/ajax', function(req, res) {
    console.log(req.body);
    python.runPython(req.body.msg);
});

app.post('/review', function(req, res) {
    review.push(req.body.review);
    res.jsonp({success:'true'});
});

app.listen(8000, function () {
    console.log('Example app listening on port 8000!');
});