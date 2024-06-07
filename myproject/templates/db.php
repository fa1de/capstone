<?php
// PostgreSQL 서버 연결 정보
$host = "localhost";
$port = "5432";
$dbname = "protocol"; // 데이터베이스명
$user = "cap"; // 사용자명
$password = "1234";

// PostgreSQL 데이터베이스에 연결
$conn = pg_connect("host=$host port=$port dbname=$dbname user=$user password=$password");

if (!$conn) {
    die("Error in connection: " . pg_last_error());
}

// 데이터베이스에서 데이터 가져오기
$query = "SELECT * FROM 테이블명"; // 가져올 데이터베이스 테이블명을 지정합니다.

$result = pg_query($conn, $query);

if (!$result) {
    die("Error in SQL query: " . pg_last_error());
}

// 결과 출력
while ($row = pg_fetch_assoc($result)) {
    echo "열1: " . $row['열1'] . ", 열2: " . $row['열2'] . "<br/>";
}

// 연결 종료
pg_close($conn);
?>
