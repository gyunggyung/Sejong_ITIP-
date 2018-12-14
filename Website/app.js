const express = require('express');
var bodyParser = require('body-parser');
var review = require('./public/js/review');

const app = express();

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended:true}));

app.use(express.static(__dirname+'/public'));
//app.use('/ajax', './js/ajax.js');
app.get('/', function (req, res) {
    res.sendFile(__dirname+"/index.html");
});

app.post('/ajax', function(req, res) {
    //python.runPython(req.body.msg);
    console.log(req.ip);
    var prepared = [3];
    var arg = prepared.concat(req.body.msg);
    let python_shell = require('python-shell');
    let options = {
        mode: 'text',
        pythonPath: "C:/Users/user/AppData/Local/conda/conda/envs/crawling/python.exe", // edit this
        pythonOptions: ['-u'],
        scriptPath: './public/python', // edit this
        args: arg
    };
    var output;
    var pyshell = new python_shell.PythonShell('recommendation.py', options);

    console.log(arg, arg.length);
    pyshell.on('message', function (message) {
        output = message;
        console.log(output);
        pyshell.childProcess.kill();
        res.send(output);
    });
});

app.post('/review', function(req, res) {
    review.push(req.body.review);
    res.jsonp({success:'true'});
});

app.listen(8000, function () {
    console.log('Server running on port 8000!');
});