<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    if (isset($_POST['name']) && !empty(trim($_POST['name']))) {
        $name = htmlspecialchars(trim($_POST['name']));
        echo "<strong>$name</strong>, believe in yourself — you are capable of amazing things! 🚀";
    } else {
        echo "Please enter your name to receive a motivational message.";
    }
} else {
    echo "Invalid request.";
}
?>
