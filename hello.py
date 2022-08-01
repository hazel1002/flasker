from crypt import methods
from flask import Flask, flash, render_template
from flask_wtf import FlaskForm
from importlib_metadata import method_cache
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


# Create a Flask Instance
app = Flask(__name__)
app.config['SECRET_KEY'] = "my super secret key that is no one is supposed to know" #create secret key

# Create an Form Class
class NamerForm(FlaskForm):
    name = StringField("What's your name?", validators=[DataRequired()])
    submit = SubmitField("Submit")


# Create a router decorator
@app.route('/')

# def index():
#     return "<h1>Hello World</h1>"

def index():
    first_name = "Hazel"
    stuff = "This is <strong>bold</strong> Text "
    flash("Welcome to Our Website!")
    favorite_fruits = ['apple','orange',34,'peach']
    return render_template("index.html",
    first_name=first_name,
    stuff=stuff,
    favorite_fruits=favorite_fruits)

# localhost:5000/user/John
@app.route('/user/<name>')
def user(name):
    return render_template("user.html", user_name=name)

# Create Custom Error Pages

# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500

# Create Name Page
@app.route('/name', methods=['GET','POST'])
def name():
    name = None
    form = NamerForm()
    # Validate Form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("Form Submitted Successfully!")
    return render_template("name.html",name = name,form = form)


