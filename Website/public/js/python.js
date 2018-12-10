exports.runPython = function (check) {
    var num = [3];
    var arg = [];
    arg = num.concat(check);
    console.log(arg, arg.length);
    let python_shell = require('python-shell');
    let options = {
        mode: 'text',
        pythonPath: "C:/Users/user/AppData/Local/conda/conda/envs/crawling/python.exe", // edit this
        pythonOptions: ['-u'],
        scriptPath: 'C:/APM_Setup/htdocs/public/python', // edit this
        args: arg
    };
    python_shell.PythonShell.run('recommendation.py', options, function (err) {
        if (err) throw err;
        console.log('finished');
    });
};