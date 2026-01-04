<?php
session_start();

if (!isset($_SESSION['username'])) {
    header("Location: login.php");
    exit();
}

$username = htmlspecialchars($_SESSION['username']);
?>

<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Welcome</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');
  body {
    font-family: 'Poppins', sans-serif;
    background: linear-gradient(120deg, #89f7fe 0%, #66a6ff 100%);
    height: 100vh;
    margin: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #222;
  }
  .welcome-box {
    background: white;
    padding: 50px 60px;
    border-radius: 20px;
    box-shadow: 0 20px 50px rgba(102, 166, 255, 0.3);
    text-align: center;
    width: 400px;
  }
  h1 {
    font-weight: 700;
    margin-bottom: 12px;
    color: #2c3e50;
  }
  p {
    font-size: 18px;
    margin-bottom: 35px;
    color: #34495e;
  }
  .logout-btn {
    background-color: #e74c3c;
    color: white;
    border: none;
    padding: 14px 0;
    font-size: 18px;
    width: 100%;
    border-radius: 12px;
    cursor: pointer;
    font-weight: 600;
    letter-spacing: 1px;
    transition: background-color 0.3s ease;
    box-shadow: 0 5px 15px rgba(231, 76, 60, 0.4);
  }
  .logout-btn:hover {
    background-color: #c0392b;
  }
</style>
</head>
<body>
  <div class="welcome-box">
    <h1>Welcome, <?php echo $username; ?>!</h1>
    <p>You have successfully signed in.</p>
    <form action="logout.php" method="POST">
      <button class="logout-btn" type="submit">Sign Out</button>
    </form>
  </div>
</body>
</html>
