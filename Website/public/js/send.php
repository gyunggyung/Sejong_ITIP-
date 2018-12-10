<?php
	header('Content-type: text/html; charset=UTF-8');
	
    $host = "localhost";
    $user = 'root';
    $pw = 'apmsetup';
    $dbName = 'review';
    $conn = mysqli_connect($host, $user, $pw, $dbName);
	$conn->query("set names utf8");
	
	$review = $_POST['review'];
	$review = $_POST['star'];
	$date = date('Y-n-j G:i:s');
	
	$stmt = $conn->prepare("INSERT INTO test (review,datetime) VALUES (?, ?, ?)");
	$stmt->bind_param("ss", $review, $star, $date);
	$stmt->execute();
	
		