from flask import Flask, request, Response, redirect, render_template, session, url_for
from helpers import metro

tiempo = 0

app = Flask(__name__)

# obteniendo el post resquest
@app.route('/api', methods=['POST'])
def api_response():
    if request.method == 'POST':
       print('post metodo')
    # Output comparison
    return "ok"

@app.route("/")
def index():
    return render_template("index.html")