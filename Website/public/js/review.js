function sendReview() {
    var str = $("#reviewContent").val();
    var star;
    var $checked = $(".star-input").find(":checked");
    var locationArr = [];
    var i;

    for (i = 0; i < 3; i++) {
        var text = $('#print' + (i + 1)).children('#Name').text();
        locationArr.push(text);
    }
    var location = locationArr.join(',');

    console.log(location);
    if ($checked.length === 0) {
        star = 0;
    } else {
        star = ($checked.next().text());
    }
    if (str.length === 0) {
        alert("리뷰를 입력해주세요");
        $("#reviewContent").focus();
    } else if (star === 0) {
        alert("별점을 선택해주세요")
    } else {
        $.ajax({
            url: 'http://localhost:8000/review',
            dataType: 'json',
            type: 'POST',
            data: {'review': [str, star, location]},
            success: function (data) {
                if (data['success'])
                    alert('리뷰가 등록되었습니다')
            }
        })
    }
}

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
    var data = [review[0], review[1], review[2], formatted];

    console.log(data);

    connection.query('INSERT INTO test (review, star, place, datetime) VALUES (?, ?, ?, ?)', [review[0], review[1], review[2], formatted], function (err, res) {
        if (err) throw err;
    });
};