from flask import Flask, render_template
import datetime

app = Flask(__name__)

@app.route("/")
def index():
    hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return render_template("index.html", hora=hora)
