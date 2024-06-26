from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)


@app.route("/")
def welcome():
    return render_template("index.html")


import os
from PIL import Image

app.config["UPLOAD_FOLDER"] = "uploads"


@app.route("/submit", methods=["POST", "GET"])
def submit():
    if request.method == "POST":
        image = request.files["imageFile"]
        filename = image.filename
        path = "static/uploads/"
        img_path = os.path.join(path, filename)
        image.save(img_path)
    return render_template("result.html", path=img_path)


if __name__ == "__main__":
    app.run(debug=True)
