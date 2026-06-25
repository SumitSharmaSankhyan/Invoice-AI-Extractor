from flask import Flask, render_template, request, jsonify, send_file
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "output"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["OUTPUT_FOLDER"] = OUTPUT_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


# -----------------------
# HOME
# -----------------------

@app.route("/")
def index():
    return render_template("index.html")


# -----------------------
# UPLOAD PDF
# -----------------------

@app.route("/upload", methods=["POST"])
def upload():

    if "files" not in request.files:
        return jsonify({
            "success": False,
            "message": "No files received"
        })

    files = request.files.getlist("files")

    uploaded = []

    for file in files:

        if file.filename == "":
            continue

        if not file.filename.lower().endswith(".pdf"):
            continue

        filename = secure_filename(file.filename)

        filepath = os.path.join(
            app.config["UPLOAD_FOLDER"],
            filename
        )

        file.save(filepath)

        uploaded.append({
            "name": filename,
            "path": filepath,
            "size": round(os.path.getsize(filepath)/1024/1024,2)
        })

    return jsonify({
        "success": True,
        "count": len(uploaded),
        "files": uploaded
    })


# -----------------------
# EXTRACT
# -----------------------

@app.route("/extract", methods=["POST"])
def extract():

    """
    OCR will be added here.

    For now this only returns blank rows.
    """

    data = request.json

    files = data["files"]

    results = []

    for file in files:

        results.append({

            "filename": file["name"],

            "vendor":"",

            "po":"",

            "invoice_no":"",

            "invoice_date":"",

            "base_amount":"",

            "igst":"",

            "cgst":"",

            "sgst":"",

            "other":"",

            "total":""

        })

    return jsonify(results)


# -----------------------
# DOWNLOAD EXCEL
# -----------------------

@app.route("/download")
def download():

    filepath = os.path.join(
        app.config["OUTPUT_FOLDER"],
        "Invoice_Output.xlsx"
    )

    if os.path.exists(filepath):

        return send_file(
            filepath,
            as_attachment=True
        )

    return "Excel not generated."


# -----------------------
# START OVER
# -----------------------

@app.route("/reset", methods=["POST"])
def reset():

    for folder in [UPLOAD_FOLDER, OUTPUT_FOLDER]:

        for file in os.listdir(folder):

            path = os.path.join(folder,file)

            if os.path.isfile(path):
                os.remove(path)

    return jsonify({
        "success":True
    })


# -----------------------

if __name__ == "__main__":
    app.run(debug=True)
