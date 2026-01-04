<?php
session_start();
session_destroy();
?>

<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Logged Out</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');
  body {
    font-family: 'Poppins', sans-serif;
    background: linear-gradient(135deg, #f6d365, #fda085);
    height: 100vh;
    margin: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #444;
  }
  .logout-container {
    background: white;
    padding: 40px 50px;
    border-radius: 18px;
    box-shadow: 0 15px 45px rgba(253, 160, 133, 0.4);
    text-align: center;
    width: 350px;
  }
  h2 {
    font-weight: 700;
    margin-bottom: 25px;
    color: #d35400;
  }
  p {
    font-size: 17px;
    margin-bottom: 35px;
    color: #7f8c8d;
  }
  .login-btn {
    background-color: #d35400;
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
    box-shadow: 0 5px 15px rgba(211, 84, 0, 0.4);
  }
  .login-btn:hover {
    background-color: #b03a02;
  }
</style>
</head>
<body>
  <div class="logout-container">
    <h2>Logged Out</h2>
    <p>You have successfully signed out. See you soon!</p>
    <a href="login.php"><button class="login-btn">Sign In Again</button></a>
  </div>
</body>
</html>
