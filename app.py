import os
import shutil
from flask import Flask, request, render_template, send_from_directory, jsonify

app = Flask(__name__)

# Directory to store uploaded files
UPLOAD_FOLDER = 'user_files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def home():
    """Render the main web interface."""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file uploads."""
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400

    # Save the uploaded file to the upload folder
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    return 'File uploaded successfully', 200

@app.route('/download/<filename>')
def download_file(filename):
    """Allow downloading of files from the server."""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/list_folder', methods=['GET'])
def list_folder():
    """List the contents of the upload folder."""
    path = request.args.get('path', UPLOAD_FOLDER)
    if os.path.exists(path):
        files = os.listdir(path)
        return jsonify(files)
    return jsonify({'error': 'Path does not exist'}), 404

@app.route('/vm_info')
def vm_info():
    """Return VM storage information (total, used, free)."""
    total, used, free = shutil.disk_usage("/")
    return jsonify({
        'total': round(total / (1024**3), 2),  # Convert bytes to GB
        'used': round(used / (1024**3), 2),
        'free': round(free / (1024**3), 2)
    })

if __name__ == '__main__':
    app.run(debug=True)
