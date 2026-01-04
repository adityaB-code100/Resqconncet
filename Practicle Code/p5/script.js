// script.js

// Function to calculate the length of a string
function calculateStringLength() {
  let str = document.getElementById("stringInput").value;
  let length = str.length;  // Get the length of the string
  document.getElementById("stringLength").textContent = length;  // Display the length in the HTML
}

// Function to reverse the digits of a number
function reverseNumber() {
  let num = document.getElementById("numberInput").value;
  
  if(num) {
    let reversedNum = num.toString().split('').reverse().join(''); // Reverse the digits
    document.getElementById("reversedNumber").textContent = reversedNum;  // Display reversed number
  } else {
    document.getElementById("reversedNumber").textContent = "Please enter a number.";
  }
}
