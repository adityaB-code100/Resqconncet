<?php
session_start();

$valid_users = [
    "admin" => "password123",
    "user1" => "pass456",
    "john" => "john789",
    "alice" => "alice321"
];

$error = "";

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $username = $_POST['username'] ?? '';
    $password = $_POST['password'] ?? '';

    if (isset($valid_users[$username]) && $valid_users[$username] === $password) {
        $_SESSION['username'] = $username;
        header("Location: welcome.php");
        exit();
    } else {
        $error = "Invalid username or password!";
    }
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Sign In</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');
  body {
    font-family: 'Poppins', sans-serif;
    background: linear-gradient(135deg, #667eea, #764ba2);
    height: 100vh;
    margin: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #333;
  }
  .login-container {
    background: white;
    padding: 40px 50px;
    border-radius: 16px;
    box-shadow: 0 15px 40px rgba(0, 0, 0, 0.2);
    width: 360px;
    text-align: center;
  }
  h2 {
    margin-bottom: 30px;
    font-weight: 600;
    color: #4a4a4a;
  }
  input[type="text"], input[type="password"] {
    width: 100%;
    padding: 14px 20px;
    margin: 15px 0 25px 0;
    border: 2px solid #ddd;
    border-radius: 10px;
    font-size: 16px;
    transition: border-color 0.3s ease;
  }
  input[type="text"]:focus, input[type="password"]:focus {
    border-color: #667eea;
    outline: none;
    box-shadow: 0 0 6px #667eea;
  }
  button {
    background-color: #667eea;
    color: white;
    border: none;
    padding: 14px 0;
    font-size: 18px;
    width: 100%;
    border-radius: 10px;
    cursor: pointer;
    font-weight: 600;
    letter-spacing: 1px;
    transition: background-color 0.3s ease;
  }
  button:hover {
    background-color: #5a67d8;
  }
  .error {
    color: #e53e3e;
    margin-bottom: 20px;
    font-weight: 600;
    background: #ffe5e5;
    padding: 10px 15px;
    border-radius: 8px;
    box-shadow: 0 2px 5px rgba(229, 62, 62, 0.3);
  }
</style>
</head>
<body>
  <div class="login-container">
    <h2>Sign In</h2>
    <?php if ($error): ?>
      <div class="error"><?php echo htmlspecialchars($error); ?></div>
    <?php endif; ?>
    <form method="POST" action="">
      <input type="text" name="username" placeholder="Username" required autocomplete="off" />
      <input type="password" name="password" placeholder="Password" required autocomplete="off" />
      <button type="submit">Sign In</button>
    </form>
  </div>
</body>
</html>
