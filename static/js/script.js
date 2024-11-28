document.querySelector('form').addEventListener('submit', function() {
    document.getElementById('loading').style.display = 'block'; // Show loading message
});

function displayFileName() {
    const fileInput = document.getElementById('file-upload');
    const fileName = fileInput.files.length > 0 ? fileInput.files[0].name : "No file chosen";
    document.getElementById('file-name').textContent = fileName;
}

// Function to handle the form validation
document.getElementById('file-form').addEventListener('submit', function(event) {
    var fileInput = document.getElementById('file-upload');
    var errorMessage = document.getElementById('error-message');

    // Check if no file is selected
    if (!fileInput.files.length) {
        // Prevent form submission
        event.preventDefault();

        // Display error message
        errorMessage.style.display = 'block';
    } else {
        // Hide error message if a file is selected
        errorMessage.style.display = 'none';
    }
});