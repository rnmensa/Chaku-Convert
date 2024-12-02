// Handle the form submission and show/hide the loading message
document.getElementById('file-form').addEventListener('submit', function (event) {
    const fileInput = document.getElementById('file-upload');
    const errorMessage = document.getElementById('error-message');
    const loadingMessage = document.getElementById('loading');

    // Form validation: Check if a file is selected
    if (!fileInput.files.length) {
        // Prevent form submission if no file is selected
        event.preventDefault();
        errorMessage.style.display = 'block'; // Show error message
        loadingMessage.style.display = 'none'; // Hide loading message (just in case)
        return;
    }
   // Hide error message and show loading message
    errorMessage.style.display = 'none';
    loadingMessage.style.display = 'block';

    // Optional: Hide the loading message after 3 seconds
    setTimeout(() => {
        loadingMessage.style.display = 'none';
    }, 3000);
});


function displayFileName() {
    const fileInput = document.getElementById('file-upload');
    const fileName = fileInput.files.length > 0 ? fileInput.files[0].name : "No file chosen";
    document.getElementById('file-name').textContent = fileName;
}

