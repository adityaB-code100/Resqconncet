<!DOCTYPE html>
<html>
<head>
    <title>PHP Digital Clock with Date</title>
    <style>
        body {
            background-color: #f0f4f8;
            color: #333;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            text-align: center;
            margin-top: 20%;
        }
        .clock {
            display: inline-block;
            padding: 15px 35px;
            border: 2px solid #4a90e2;
            border-radius: 10px;
            background-color: #e6f0fa;
            letter-spacing: 6px;
            box-shadow: 2px 2px 6px rgba(74, 144, 226, 0.3);
            user-select: none;
        }
        .date {
            font-size: 24px;
            margin-bottom: 10px;
            letter-spacing: normal;
        }
        .time {
            font-size: 48px;
            letter-spacing: 6px;
        }
    </style>
    <meta http-equiv="refresh" content="1"> <!-- Refresh page every 1 second -->
</head>
<body>

<div class="clock">
    <div class="date">
        <?php
        date_default_timezone_set("Asia/Kolkata"); // Set your server timezone
        echo date("l, F j, Y"); // e.g. Monday, June 6, 2025
        ?>
    </div>
    <div class="time">
        <?php
        echo date("h:i:s A"); // Display time in HH:MM:SS AM/PM format
        ?>
    </div>
</div>

</body>
</html>
