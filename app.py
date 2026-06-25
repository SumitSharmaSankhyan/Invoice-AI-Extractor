from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():

    if "files" not in request.files:
        return jsonify({"success": False, "message": "No files received"})

    files = request.files.getlist("files")

    uploaded = []

    for file in files:

        if file.filename == "":
            continue

        save_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)

        file.save(save_path)

        uploaded.append(file.filename)

    return jsonify({
        "success": True,
        "files": uploaded
    })


if __name__ == "__main__":
    app.run(debug=True)
