<?php
// DB Connection
$conn = new mysqli("localhost", "root", "", "student_db");

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$output = "";
if (isset($_POST['query'])) {
    $search = $conn->real_escape_string($_POST['query']);

    $sql = "SELECT * FROM students 
            WHERE name LIKE '%$search%' OR roll LIKE '%$search%'";

    $result = $conn->query($sql);

    if ($result->num_rows > 0) {
        $output .= "<table>
                    <tr><th>ID</th><th>Name</th><th>Roll No</th><th>Branch</th></tr>";
        while ($row = $result->fetch_assoc()) {
            $output .= "<tr>
                        <td>{$row['id']}</td>
                        <td>{$row['name']}</td>
                        <td>{$row['roll']}</td>
                        <td>{$row['branch']}</td>
                    </tr>";
        }
        $output .= "</table>";
    } else {
        $output = "No student found.";
    }
}
echo $output;
$conn->close();
?>
