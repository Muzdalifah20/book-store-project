from flask import Flask , request
from utilities import get_html , usersdb
import json

app = Flask(__name__)

@app.route("/")
def index():
    return get_html("index")