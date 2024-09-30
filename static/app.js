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
        loadFolderContents(); // Refresh folder contents after upload
    })
    .catch(error => console.error('Error:', error));
}

function loadFolderContents() {
    fetch('/list_folder')
    .then(response => response.json())
    .then(files => {
        const folderContentDiv = document.getElementById('folderContent');
        folderContentDiv.innerHTML = '<ul>';
        files.forEach(file => {
            folderContentDiv.innerHTML += `<li><a href="/download/${file}" download>${file}</a></li>`;
        });
        folderContentDiv.innerHTML += '</ul>';
    })
    .catch(error => console.error('Error:', error));
    
    // Fetch VM capacity information
    fetch('/vm_info')
    .then(response => response.json())
    .then(data => {
        const vmInfoDiv = document.getElementById('vmInfo');
        vmInfoDiv.innerHTML = `
            <strong>Capacity:</strong><br>
            Total: ${data.total} GB<br>
            Used: ${data.used} GB<br>
            Free: ${data.free} GB
        `;
    })
    .catch(error => console.error('Error fetching VM info:', error));
}

window.onload = loadFolderContents;
