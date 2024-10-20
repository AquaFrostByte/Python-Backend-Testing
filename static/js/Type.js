var i = 0;
var txt = 'Time for all of us';
var speed = 100;

function typeWriter() {
  if (i < txt.length) {
    document.getElementById("Header1").innerHTML += txt.charAt(i);
    i++;
    setTimeout(typeWriter, speed);
  }
}

window.onload = function() {
    typeWriter();
};