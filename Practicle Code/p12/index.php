<?php
// DB connection
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "student_db";

$conn = new mysqli($servername, $username, $password, $dbname);
if ($conn->connect_error) die("Connection failed: " . $conn->connect_error);

// Check if "sort" button clicked
$sorted = isset($_GET['sort']) && $_GET['sort'] == 'asc';

// Prepare SQL query
if ($sorted) {
    $sql = "SELECT * FROM students ORDER BY name ASC";
} else {
    $sql = "SELECT * FROM students";
}

$result = $conn->query($sql);
?>

<!DOCTYPE html>
<html>
<head>
    <title>Sort Students Ascending</title>
    <style>
        body { font-family: Arial; padding: 20px; background: #fafafa; }
        table { border-collapse: collapse; margin: 20px auto; width: 70%; background: #fff; box-shadow: 0 0 10px #ccc; }
        th, td { padding: 10px; border: 1px solid #ddd; text-align: center; }
        th { background-color: #5cb85c; color: white; }
        .btn {
            display: block;
            width: 150px;
            margin: 20px auto;
            padding: 10px;
            background-color: #5cb85c;
            color: white;
            font-weight: bold;
            text-align: center;
            text-decoration: none;
            border-radius: 5px;
            cursor: pointer;
        }
        .btn:hover { background-color: #4cae4c; }
    </style>
</head>
<body>

<a href="?sort=asc" class="btn">Sort Ascending</a>

<table>
    <thead>
        <tr><th>ID</th><th>Name</th><th>Roll No.</th><th>Branch</th></tr>
    </thead>
    <tbody>
    <?php
    if ($result && $result->num_rows > 0) {
        while ($row = $result->fetch_assoc()) {
            echo "<tr>
                <td>" . htmlspecialchars($row['id']) . "</td>
                <td>" . htmlspecialchars($row['name']) . "</td>
                <td>" . htmlspecialchars($row['roll']) . "</td>
                <td>" . htmlspecialchars($row['branch']) . "</td>
            </tr>";
        }
    } else {
        echo "<tr><td colspan='4'>No records found.</td></tr>";
    }
    $conn->close();
    ?>
    </tbody>
</table>

</body>
</html>
