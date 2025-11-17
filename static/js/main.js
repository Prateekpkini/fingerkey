// main.js — handles drag & drop, file preview and small UI helpers

document.addEventListener('DOMContentLoaded', () => {
  const dropArea = document.getElementById('drop-area');
  const fileInput = document.getElementById('fileInput');
  const selectedFile = document.getElementById('selectedFile');

  if (!dropArea || !fileInput) return;

  // show filename when user selects via dialog
  fileInput.addEventListener('change', (e) => {
    const f = e.target.files && e.target.files[0];
    selectedFile.textContent = f ? f.name : 'No file selected';
  });

  // handle clicks on the drop area
  dropArea.addEventListener('click', () => fileInput.click());

  // prevent default behaviors for drag/drop
  ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, (e) => {
      e.preventDefault();
      e.stopPropagation();
    });
  });

  dropArea.addEventListener('dragover', () => {
    dropArea.classList.add('drag-over');
  });
  dropArea.addEventListener('dragleave', () => {
    dropArea.classList.remove('drag-over');
  });

  dropArea.addEventListener('drop', (e) => {
    const dt = e.dataTransfer;
    const files = dt.files;
    if (files && files.length) {
      fileInput.files = files; // assign dropped files to input
      const f = files[0];
      selectedFile.textContent = f.name;
    }
    dropArea.classList.remove('drag-over');
  });
});
