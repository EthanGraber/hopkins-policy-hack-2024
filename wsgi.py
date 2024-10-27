import os

import zipfile
import tempfile
import pathlib
import sqlite3
from flask import Flask, abort, request, render_template, jsonify

from patrick_file import analyze_fitbit_activity
from llm import generate_notification_with_examples

app = Flask(__name__)

# Create a directory to store the uploaded files
UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

DATABASE_NAME = "nudge_results.db"
TABLE_NAME = "feedback"
USER_ID="1503960366"

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_file():
    if not "file" in request.files:
        abort(400, description="Bad Request: no file")
    file = request.files["file"]

    if not zipfile.is_zipfile(os.path.join(UPLOAD_DIR, file.filename)):
        abort(400, description="Bad Request: expecting fitbit data zip")

    with tempfile.TemporaryDirectory() as tmp_dir:
        with zipfile.ZipFile(os.path.join(UPLOAD_DIR, file.filename)) as zip_ref:
            zip_ref.extractall(tmp_dir)

        resp = analyze_fitbit_activity(pathlib.Path(tmp_dir) / USER_ID)

        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()
            query = f"UPDATE {TABLE_NAME} SET increase = ? WHERE user_id = ? AND id = (SELECT MAX(id) FROM {TABLE_NAME} WHERE user_id = ?)"
            cursor.execute(query, (resp, USER_ID, USER_ID))
            conn.commit()



    return {"message": f"File uploaded: {file.filename}"}


@app.route("/send-test-notification")
def send_test_notification():
    """
    Fetch data from SQLite database and return it as JSON.
    """

    try:
        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()

            # Fetch data from the database
            query = f"SELECT * FROM {TABLE_NAME} WHERE user_id = {USER_ID} AND increase=True"
            cursor.execute(query)
            rows = cursor.fetchall()
            column_names = [description[0] for description in cursor.description]

            # Convert the result to a list of dictionaries
            data = [dict(zip(column_names, row)) for row in rows]

            notification = generate_notification_with_examples(data)

            query = "INSERT INTO feedback (user_id, message) VALUES (?, ?)"
            cursor.execute(query, (USER_ID, notification))
            conn.commit()

            return {"message":notification}

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return {"message": "Error fetching data"}, 500


@app.route("/static/<path:path>")
def send_static(path):
    return app.send_static_file(path)


if __name__ == "__main__":
    app.run(debug=True)
