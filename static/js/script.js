

a="/service"
  const sentences = [
    { text: "Emergency assistance at your fingertips", href: a },
    { text: "Stay safe, we are here to help", href: a},
    { text: "Call 1091 for Women Helpline", href: a },
    { text: "In case of fire, dial 101 immediately", href: a },
    { text: "Help is just a call away", href: a }
  ];

  let index = 0;
  const container = document.getElementById("floatingSentence");

  function scrollSentence() {
    const { text, href } = sentences[index];
    container.innerHTML = `<a href="${href}" target="_blank">${text}</a>`;
    const link = container.querySelector("a");

    let leftPos = window.innerWidth;
    link.style.left = leftPos + "px";

    function animate() {
      leftPos -= 1;
      link.style.left = leftPos + "px";

      if (leftPos + link.offsetWidth > 0) {
        requestAnimationFrame(animate);
      } else {
        index = (index + 1) % sentences.length;
        setTimeout(scrollSentence, 500);
      }
    }

    animate();
  }

  scrollSentence();



  //card

  window.addEventListener("DOMContentLoaded", () => {
    const cards = document.querySelectorAll(".card");

    cards.forEach((card, index) => {
      setTimeout(() => {
        card.style.opacity = "1";
        card.style.transform = "translateY(0)";
      }, index * 1000); // Delay each card
    });
  });

function validateForm() {
    let isValid = true;

    // Clear previous errors
    document.querySelectorAll('span[id$="Error"]').forEach(span => span.textContent = '');

    // Name validation
    const name = document.getElementById("name").value.trim();
    if (name.length < 2) {
        document.getElementById("nameError").textContent = "Name must be at least 2 characters.";
        isValid = false;
    }

    // Contact validation
    const contact = document.getElementById("contact").value.trim();
    const contactPattern = /^[6-9]\d{9}$/;
    if (!contactPattern.test(contact)) {
        document.getElementById("contactError").textContent = "Please enter a valid 10-digit mobile number starting with 6-9.";
        isValid = false;
    }

    // Emergency type
    const emergency = document.getElementById("emergency").value.trim();
    if (emergency === "") {
        document.getElementById("emergencyError").textContent = "Please enter the type of emergency.";
        isValid = false;
    }

    // Location validation
    const location = document.getElementById("location").value.trim();
    if (location.length < 3) {
        document.getElementById("locationError").textContent = "Location must be at least 3 characters.";
        isValid = false;
    }

    // Description validation
     const description = document.getElementById("description").value.trim();
    if (description.length < 10) {
        document.getElementById("descriptionError").textContent = "Description must be at least 10 characters.";
        isValid = false;
    } 
    if (isValid) {
        alert("Complaint submitted successfully!");
    }

    return isValid;
}
function validateContactForm() {
    let isValid = true;

    // Clear previous error messages
    document.querySelectorAll('span[id$="Error"]').forEach(span => span.textContent = '');

    // Name Validation
    const name = document.getElementById("name").value.trim();
    if (name.length < 2) {
        document.getElementById("nameError").textContent = "Please enter a valid name (min 2 characters).";
        isValid = false;
    }

    // Contact Validation
    const contact = document.getElementById("contact").value.trim();
    const contactPattern = /^[6-9]\d{9}$/;
    if (!contactPattern.test(contact)) {
        document.getElementById("contactError").textContent = "Enter a valid 10-digit mobile number starting with 6-9.";
        isValid = false;
    }

    // Location Validation
    const location = document.getElementById("location").value.trim();
    if (location.length < 3) {
        document.getElementById("locationError").textContent = "Please provide a valid location.";
        isValid = false;
    }

    // Description Validation
    const description = document.getElementById("description").value.trim();
    if (description.length < 10) {
        document.getElementById("descriptionError").textContent = "Description must be at least 10 characters.";
        isValid = false;
    }
    if (isValid) {
        alert("Contact Request submitted successfully!");
    }

    return isValid;
}

