from flask import Flask, render_template, url_for, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from serp_api import fetch_data

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'
db = SQLAlchemy(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(30), nullable=False, unique=True)
    lastname = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)

class SignUpForm(FlaskForm):
    firstname = StringField(validators=[InputRequired(), Length(min=1, max=30)], render_kw={"placeholder": "FirstName"})
    lastname = StringField(validators=[InputRequired(), Length(min=1, max=20)], render_kw={"placeholder": "LastName"})
    email = EmailField(validators=[InputRequired(), Length(min=6, max=80)], render_kw={"placeholder": "Email"})
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField('SignUp')

    def validate_email(self, email):
        existing_user_email = User.query.filter_by(email=email.data).first()
        if existing_user_email:
            raise ValidationError('That email already exists. Please use another one.')

class LoginForm(FlaskForm):
    firstname = StringField(validators=[InputRequired(), Length(min=1, max=30)], render_kw={"placeholder": "FirstName"})
    lastname = StringField(validators=[InputRequired(), Length(min=1, max=20)], render_kw={"placeholder": "LastName"})
    email = EmailField(validators=[InputRequired(), Length(min=6, max=80)], render_kw={"placeholder": "Email"})
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField('Login')


@app.route("/")
def home():
    return render_template('home.html', active_page='home')

@app.route('/search',methods=['GET'])
def fetch_search_data():
    keyword = request.args.get("keyword")
    type = request.args.get("type")
    data_list = fetch_data(keyword,type)
    if not data_list:
        error_message = "No results found for the given keyword and type."
        print(data_list, error_message)
        return jsonify(error_message=error_message)
    return jsonify(data_list)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html', form=form, active_page='login')

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    return render_template('signup.html', form=form, active_page='signup')

if __name__ == '__main__':
    app.run(debug="True")