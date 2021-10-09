import os
import requests
from flask import Flask, render_template, request, session, redirect
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect, generate_csrf
from back_census.config import Config
from datetime import datetime


app = Flask(__name__)
app.config.from_object(Config)


# Application Security
CORS(app)


@app.after_request
def inject_csrf_token(response):
    response.set_cookie(
        'csrf_token',
        generate_csrf(),
        secure=True if os.environ.get('FLASK_ENV') else False,
        samesite='Strict' if os.environ.get('FLASK_ENV') else None,
        httponly=True)
    return response


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def react_root(path):
    print("path", path)
    if path == 'favicon.ico':
        return app.send_static_file('favicon.ico')
    return app.send_static_file('index.html')


@app.route('/')
def census():
    CENSUS_KEY = os.environ.get('CENSUS_KEY')
    URL = 'https://api.census.gov/data/2019/pep/population'
    PARAMS = {"get": "NAME,POP", "for": {"place": "*"}, "key": CENSUS_KEY}
    response = requests.get(url = URL, params = PARAMS)
    data = response.json()
    return {"data": data}
