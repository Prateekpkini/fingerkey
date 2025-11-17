document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('fileInput');
    if (fileInput) {
        fileInput.addEventListener('change', (e) => {
            const fileName = e.target.files[0] ? e.target.files[0].name : 'Select an image file (JPG, PNG, BMP).';
            const fileLabel = document.querySelector(`label[for='${fileInput.id}']`);
            if(fileLabel) {
                fileLabel.textContent = fileName;
            }
        });
    }
});