from flask import Flask, render_template, request, redirect, url_for, jsonify, send_from_directory
import os
import shutil
import socket

app = Flask(__name__)
app.secret_key = 'secret'

UPLOAD_FOLDER = 'uploads'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    file_list = os.listdir(UPLOAD_FOLDER)
    return render_template('index.html', files=file_list)

@app.route('/files')
def files():
    file_list = os.listdir(UPLOAD_FOLDER)
    return jsonify(file_list)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'files' not in request.files:
        return redirect(request.url)
    file_list = request.files.getlist('files')
    for file in file_list:
        if file:
            file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/refresh')
def refresh():
    shutil.rmtree(UPLOAD_FOLDER)
    os.makedirs(UPLOAD_FOLDER)
    return redirect(url_for('index'))

def get_ip_address():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
