from flask import Flask, abort, request, render_template
import os

import zipfile
import tempfile
import pathlib

from patrick_file import process_folder

app = Flask(__name__)

# Create a directory to store the uploaded files
UPLOAD_DIR = 'uploads'
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" in request.files:
        file = request.files["file"]

    # Check if the uploaded file is a zip
    if not zipfile.is_zipfile(os.path.join(UPLOAD_DIR, file.filename)):
        abort(400, description="Bad Request: expecting fitbit data zip")

    # Create a temporary folder to extract the zip
    with tempfile.TemporaryDirectory() as tmp_dir:
        # Extract the zip to the temporary folder
        with zipfile.ZipFile(os.path.join(UPLOAD_DIR, file.filename)) as zip_ref:
            zip_ref.extractall(tmp_dir)
        
        # Call process_folder with a pathlib.Path argument to the temporary folder
        resp = process_folder(pathlib.Path(tmp_dir))
    return {"message": "File uploaded!", "status": resp}



@app.route("/send-test-notification")
def log_to_console():
    print("Button clicked!")
    return {"message": "pong!"}

@app.route('/static/<path:path>')
def send_static(path):
    return app.send_static_file(path)

if __name__ == "__main__":
    app.run(debug=True)
