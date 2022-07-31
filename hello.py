from flask import Flask, render_template


# Create a Flask Instance
app = Flask(__name__)

# Create a router decorator
@app.route('/')

# def index():
#     return "<h1>Hello World</h1>"

def index():
    first_name = "Hazel"
    stuff = "This is <strong>bold</strong> Text "
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
