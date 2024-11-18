document.querySelector('form').addEventListener('submit', function() {
    document.getElementById('loading').style.display = 'block'; // Show loading message
});

function displayFileName() {
    const fileInput = document.getElementById('file-upload');
    const fileName = fileInput.files.length > 0 ? fileInput.files[0].name : "No file chosen";
    document.getElementById('file-name').textContent = fileName;
}