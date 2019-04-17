from flask import Flask, render_template
import time
from helpers import metro


app = Flask(__name__)

@app.route("/")
def index():
    x = metro( 1)
    return render_template("index.html", x=x)