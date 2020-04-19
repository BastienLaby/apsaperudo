from flask import render_template, request

from apsaperudo.application import app


@app.route("/")
def home():
    return render_template("home.html")

