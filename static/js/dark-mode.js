document.addEventListener("DOMContentLoaded", function() {
    const checkbox = document.getElementById("dark-mode");
    const stylesheet = document.getElementById("stylesheet")
    checkbox.addEventListener('click', function() {
        if (checkbox.checked) {
            // Switch to dark mode CSS
            stylesheet.href = "/static/css/style_white.css";
        } else {
            // Switch back to light mode CSS
            stylesheet.href = "/static/css/style.css";
        }
    });
});