exports.runPython = function (check) {
    var prepared = [3];
    var arg = prepared.concat(check);
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
        return output
    });
};