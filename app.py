# app.py
import os
from flask import Flask, request, render_template, send_from_directory, jsonify

app = Flask(__name__)

# Directory to store files
UPLOAD_FOLDER = 'user_files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def home():
    return render_template('index.html')

# Endpoint to upload files
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    return 'File uploaded successfully', 200

# Endpoint to serve files
@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Endpoint to list folder contents
@app.route('/list_folder', methods=['GET'])
def list_folder():
    path = request.args.get('path', UPLOAD_FOLDER)
    if os.path.exists(path):
        files = os.listdir(path)
        return jsonify(files)
    return jsonify({'error': 'Path does not exist'}), 404

# Start the Flask app
if __name__ == '__main__':
    app.run(debug=True)
