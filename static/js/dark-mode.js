document.addEventListener("DOMContentLoaded", function() {
    const checkbox = document.getElementById("dark-mode");
    const stylesheet = document.getElementById("stylesheet")
    const stylesheet_upload = document.getElementById("stylesheet_upload")
    checkbox.addEventListener('click', function() {
        if (checkbox.checked) {
            // Switch to dark mode CSS
            stylesheet.href = "/static/css/style_white.css";
        } else {
            // Switch back to light mode CSS
            stylesheet.href = "/static/css/style.css";
        }
    });
    checkbox.addEventListener('click', function() {
        if (checkbox.checked) {
            // Switch to dark mode CSS
            stylesheet_upload.href = "/static/css/upload_white.css";
        } else {
            // Switch back to light mode CSS
            stylesheet_upload.href = "/static/css/upload.css";
        }
    });
});