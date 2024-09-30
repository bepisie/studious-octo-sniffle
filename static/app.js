// static/app.js
function uploadFile() {
    const input = document.getElementById('fileInput');
    const file = input.files[0];

    if (!file) {
        alert('Please select a file');
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.text())
    .then(data => {
        alert(data);
        loadFolderContents(); // Refresh folder contents
    })
    .catch(error => console.error('Error:', error));
}

function loadFolderContents() {
    fetch('/list_folder')
    .then(response => response.json())
    .then(files => {
        const folderContentDiv = document.getElementById('folderContent');
        folderContentDiv.innerHTML = '';
        files.forEach(file => {
            const fileElement = document.createElement('div');
            fileElement.textContent = file;
            folderContentDiv.appendChild(fileElement);
        });
    })
    .catch(error => console.error('Error:', error));
}

window.onload = loadFolderContents;
