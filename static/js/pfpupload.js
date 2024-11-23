// Handle form submission
$('#uploadForm').on('submit', function(event) {
    event.preventDefault();
    
    // Create FormData object to hold the file data
    var formData = new FormData(this);
    
    // Make an AJAX request to upload the file
    $.ajax({
        url: '/upload',
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        success: function(response) {
            // If the file is successfully uploaded, update the profile picture
            if (response.image_url) {
                $('#pfp').attr('src', response.image_url).show();
            }
        },
        error: function() {
            alert('An error occurred while uploading the file.');
        }
    });
});