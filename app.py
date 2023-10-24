from flask import Flask, render_template, url_for
app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html', active_page='home')

@app.route("/login")
def login():
    return render_template('login.html', active_page='login')

@app.route("/signup")
def signup():
    return render_template('signup.html', active_page='signup')

if __name__ == '__main__':
    app.run(debug="True")