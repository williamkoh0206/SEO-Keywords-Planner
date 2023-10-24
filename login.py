from flask import Flask, redirect, url_for
app = Flask(__name__)

@app.route('/login')
def login_function():
    pass