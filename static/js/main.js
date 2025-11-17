document.addEventListener('DOMContentLoaded', () => {
    document.body.classList.add('loaded');

    const uploadForm = document.getElementById('uploadForm');
    if (uploadForm) {
        uploadForm.addEventListener('submit', (e) => {
            const spinner = document.getElementById('spinner');
            const predictBtn = document.getElementById('predictBtn');
            if (predictBtn) predictBtn.disabled = true;
            if (spinner) {
                spinner.hidden = false;
                spinner.setAttribute('aria-hidden', 'false');
            }
        });
    }

    const resultSection = document.getElementById('result');
    if (resultSection) {
        resultSection.scrollIntoView({ behavior: 'smooth' });
    }
});