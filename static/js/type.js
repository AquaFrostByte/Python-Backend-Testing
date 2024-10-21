var i = 0;
var speed = 100; // Speed in milliseconds

function typeWriter() {
  var header = document.getElementById("Header1");

  if (header) {
    var txt = header.getAttribute("data-text"); // Get text from the data-text attribute

    if (i < txt.length) {
      header.innerHTML += txt.charAt(i); // Add one character at a time
      i++;
      setTimeout(typeWriter, speed); // Recursive call to continue typing
    }
  }
}

// Start typing when the page loads

window.onload = function() {
  typeWriter(); 
};
