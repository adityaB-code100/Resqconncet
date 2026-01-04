<?php
// File where visitor count is stored
$file = "counter.txt";

// Check if file exists, if not create and initialize with 0
if (!file_exists($file)) {
    file_put_contents($file, "0");
}

// Read the current count
$count = (int)file_get_contents($file);

// Increment the count by 1
$count++;

// Save the updated count back to the file
file_put_contents($file, $count);
?>

<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Visitor Counter</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

  body {
    margin: 0;
    padding: 0;
    font-family: 'Roboto', sans-serif;
    background: linear-gradient(135deg, #667eea, #764ba2);
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    color: #fff;
    text-align: center;
  }

  .container {
    background: rgba(255, 255, 255, 0.1);
    padding: 50px 80px;
    border-radius: 20px;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.3);
    max-width: 400px;
  }

  h1 {
    font-size: 3rem;
    margin-bottom: 20px;
    letter-spacing: 2px;
  }

  p {
    font-size: 1.8rem;
    background: #fff;
    color: #764ba2;
    padding: 15px 30px;
    border-radius: 15px;
    display: inline-block;
    box-shadow: 0 5px 15px rgba(118, 75, 162, 0.5);
    font-weight: 700;
    user-select: none;
  }

  @media (max-width: 480px) {
    .container {
      padding: 40px 30px;
      max-width: 90%;
    }
    h1 {
      font-size: 2.4rem;
    }
    p {
      font-size: 1.5rem;
      padding: 12px 20px;
    }
  }
</style>
</head>
<body>
  <div class="container">
    <h1>Welcome to Our Website</h1>
    <p>You are visitor number: <strong><?php echo $count; ?></strong></p>
  </div>
</body>
</html>
