document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('fileInput');
    const dropArea = document.getElementById('drop-area');
    const selectedFile = document.getElementById('selectedFile');
    const previewImg = document.getElementById('previewImg');
    const predictBtn = document.getElementById('predictBtn');
    const spinner = document.getElementById('spinner');

    let objectUrl = null;

    function updatePreview(file) {
        if (!file) {
            selectedFile.textContent = 'No file selected';
            if (previewImg) previewImg.hidden = true;
            return;
        }
        selectedFile.textContent = file.name;
        if (previewImg) {
            if (objectUrl) URL.revokeObjectURL(objectUrl);
            objectUrl = URL.createObjectURL(file);
            previewImg.src = objectUrl;
            previewImg.hidden = false;
        }
    }

    if (fileInput) {
        fileInput.addEventListener('change', (e) => {
            const file = e.target.files && e.target.files[0];
            updatePreview(file);
            if (predictBtn) predictBtn.disabled = !file;
        });
    }

    if (dropArea) {
        ['dragenter', 'dragover'].forEach(evt => {
            dropArea.addEventListener(evt, (e) => {
                e.preventDefault();
                dropArea.classList.add('drag-over');
            });
        });
        ['dragleave', 'drop'].forEach(evt => {
            dropArea.addEventListener(evt, (e) => {
                e.preventDefault();
                dropArea.classList.remove('drag-over');
            });
        });

        dropArea.addEventListener('drop', (e) => {
            const dt = e.dataTransfer;
            const files = dt.files;
            if (files && files.length) {
                fileInput.files = files;
                updatePreview(files[0]);
                if (predictBtn) predictBtn.disabled = false;
            }
        });
    }

    const uploadForm = document.getElementById('uploadForm');
    if (uploadForm) {
        uploadForm.addEventListener('submit', (e) => {
            // show spinner and disable submit to prevent double posts
            if (predictBtn) predictBtn.disabled = true;
            if (spinner) {
                spinner.hidden = false;
                spinner.setAttribute('aria-hidden', 'false');
            }
        });
    }
});