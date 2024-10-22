const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('file-input');
const form = document.getElementById('file-upload-form');
const spinner = document.querySelector('.spinner');  // Use querySelector for class

// Function to show spinner
function showSpinner() {
    if (spinner) {  // Check if spinner exists
        spinner.style.display = 'block';
    }
}

// Function to hide spinner
function hideSpinner() {
    if (spinner) {  // Check if spinner exists
        spinner.style.display = 'none';
    }
}

// Add click event to open file input dialog when clicking the drop zone
dropZone.addEventListener('click', () => fileInput.click());

// Handle file selection via drag-and-drop
dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();  // Prevent default behavior (Prevent file from being opened)
    dropZone.classList.add('hover');  // Visual feedback
});

dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('hover');
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('hover');

    // Get the files that were dropped
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        fileInput.files = files;  // Attach the dropped files to the file input element
        showSpinner();  // Show the spinner when upload starts
        form.submit();  // Submit the form automatically
    }
});

// Handle file selection via normal file input
fileInput.addEventListener('change', () => {
    showSpinner();  // Show the spinner when upload starts
    form.submit();  // Submit the form if a file is selected via the file input dialog
});

// Optional: Hide spinner when the form is loaded (if it's a post-back scenario)
document.addEventListener("DOMContentLoaded", hideSpinner);
