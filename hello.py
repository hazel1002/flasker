from crypt import methods
import email
from email.policy import default
from inspect import Attribute
from tkinter.tix import Tree
from turtle import title
from wsgiref.validate import validator
from xmlrpc.client import DateTime
from flask import Flask, flash, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from importlib_metadata import method_cache
from sqlalchemy import null
from wtforms import StringField, SubmitField, EmailField, IntegerField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms.widgets import TextArea


# Create a Flask Instance
app = Flask(__name__)
# Add MYSQL Database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:12345678@localhost:3306/user"
# SECRET KEY!
app.config['SECRET_KEY'] = "my super secret key that is no one is supposed to know" #create secret key
# Initialize The Database
db = SQLAlchemy(app)
migrate = Migrate(app,db)

# Create a Blog Post model
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    author = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    slug = db.Column(db.String(255))



# Create a Blog Form
class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = StringField("Content", validators=[DataRequired()], widget=TextArea())
    author = StringField("Author", validators=[DataRequired()])
    slug = StringField("Slug", validators=[DataRequired()])
    submit = SubmitField("Submit")

@app.route('/posts')
def posts():
    # Grab all the posts from database
    posts = Posts.query.order_by(Posts.date_posted)
    return render_template("posts.html", posts=posts)

@app.route('/posts/<int:id>')
def post(id):
    post = Posts.query.get_or_404(id)
    return render_template('post.html',post=post)

@app.route('/posts/edit/<int:id>', methods=['GET','POST'])
def edit_post(id):
    post = Posts.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.author = form.author.data
        post.slug = form.slug.data
        post.content = form.content.data
        # UpdateDatabase
        db.session.add(post)
        db.session.commit()
        flash("Post Has Been Updated!")
        return redirect(url_for('post',id=id))
    form.title.data = post.title
    form.author.data = post.author
    form.slug.data = post.slug
    form.content.data = post.content
    return render_template('edit_post.html',form=form)


# Add Post Page
@app.route('/add-post', methods=['GET','POST'])
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Posts(title=form.title.data,content=form.content.data,author=form.author.data,slug=form.slug.data)
        # Clear The Form
        form.title.data= ''
        form.content.data= ''
        form.author.data= ''
        form.slug.data= ''

        # Add post data to database
        db.session.add(post)
        db.session.commit()

        # Return a Message
        flash("Blog Post Submitted Successfully!")
    # Return to the webpage
    return render_template("add_post.html", form=form)


# Json Thing
@app.route('/date')
def get_current_date():
	favorite_pizza = {
		"John": "Pepperoni",
		"Mary": "Cheese",
		"Tim": "Mushroom"
	}
	return favorite_pizza
	#return {"Date": date.today()}


# Create Model
class Users(db.Model):
    userid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False)
    bankername = db.Column(db.String(200), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    userage = db.Column(db.Integer,nullable=False)
    phonenumber = db.Column(db.String(10),nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    loantype = db.Column(db.String(200), nullable=False)
    loanAMT = db.Column(db.Integer,nullable=False)
    AMT_child = db.Column(db.String(10))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    # Do some passward stuff!
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute!')
    @password.setter
    def password(self, password):
        self.password_hash =generate_password_hash(password)
    def verify_password(self,password):
        return check_password_hash(self.password_hash, password)


    # Create A String
    def __repr__(self):
        return '<Name %r>' %self.username

    # userid="123456" : 用戶ID 
    # bankername="Skye" : 銀行員帳號名稱
    # username="Skye" : 客戶名稱
    # gender="F": 客戶性別
    # userage="18" : 客戶年齡
    # phonenumber="#": 客戶電話
    # email="#" : 客戶Email
    # loantype="POS": 客戶申請類別
    # loanAMT="100000" : 客戶申請金額
    # score="80" : 客戶評估分數
    # results=result : 加裝示範從資料庫收集的資料

# Create an Form Class
class PasswordForm(FlaskForm):
    email = StringField("What's your email?", validators=[DataRequired()])
    password_hash = PasswordField("What's your password?", validators=[DataRequired()])
    submit = SubmitField("Submit")

# Create an Form Class
class NamerForm(FlaskForm):
    name = StringField("What's your name?", validators=[DataRequired()])
    submit = SubmitField("Submit")

# Create an Form Class
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    bankername = StringField("Bankername", validators=[DataRequired()])
    gender = StringField("Gender", validators=[DataRequired()])
    userage = IntegerField("Userage", validators=[DataRequired()])
    phonenumber = IntegerField("phonenumber", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    loantype = StringField("loantype", validators=[DataRequired()])
    loanAMT = IntegerField("loanAMT", validators=[DataRequired()])
    AMT_child = StringField("AMT_child")
    password_hash = PasswordField("Password", validators=[DataRequired(),EqualTo('password_hash2',message='Password Must Match!')])
    password_hash2 = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("Submit")


# Delete Database Records
@app.route('/delete/<int:id>')
def delete(id):
    user_to_delete = Users.query.get_or_404(id)
    name = None
    form = UserForm() 
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User Deleted Successfully!")
        our_users = Users.query.order_by(Users.date_added)
        return render_template("add_user.html",form=form, name=name, our_users=our_users)
    except:
        db.session.rollback()
        flash("Woops! There was a problem deleting user, try again! ")
        return render_template("add_user.html",form=form, name=name, our_users=our_users)




# Update Database Record
@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.username = request.form['name']
        name_to_update.bankername = request.form['bankername']
        name_to_update.gender = request.form['gender']
        name_to_update.userage = request.form['userage']
        name_to_update.phonenumber = request.form['phonenumber']
        name_to_update.email = request.form['email']
        name_to_update.loantype = request.form['loantype']
        name_to_update.loanAMT = request.form['loanAMT']
        name_to_update.AMT_child = request.form['AMT_child']
        try:
            db.session.commit()
            flash("User Updated Successfully!")
            return render_template("update.html", form=form, name_to_update=name_to_update, id=id)
        except:
            db.session.rollback()
            flash("Error! Looks like there was a problem...try again!")
            return render_template("update.html", form=form, name_to_update=name_to_update, id=id)
    else:
        return render_template("update.html", form=form, name_to_update=name_to_update, id=id)
 





# def index():
#     return "<h1>Hello World</h1>"

@app.route('/user/add',methods=['GET','POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            # Hash the password!!!
            hashd_pw = generate_password_hash(form.password_hash.data, "sha256") #sha256一種獲得專利的加密散列函數，它輸出一個 256 位長的值
            user = Users(username=form.name.data, bankername=form.bankername.data,
            gender=form.gender.data, userage=form.userage.data, phonenumber=form.phonenumber.data, email=form.email.data, loantype=form.loantype.data, loanAMT=form.loanAMT.data, AMT_child=form.AMT_child.data, password_hash=hashd_pw )
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.bankername.data = ''
        form.gender.data = ''
        form.userage.data = ''
        form.phonenumber.data = ''
        form.email.data = ''
        form.loantype.data = ''
        form.loanAMT.data = ''
        form.AMT_child.data = ''
        form.password_hash.data = ''
        flash("User Added Successfully!!")
    our_users = Users.query.order_by(Users.date_added)
    return render_template("add_user.html",form=form, name=name, our_users=our_users)

# Create a router decorator
@app.route('/')
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


# Create Password Test Page
@app.route('/test_pw', methods=['GET', 'POST'])
def test_pw():
	email = None
	password = None
	pw_to_check = None
	passed = None
	form = PasswordForm()
	# Validate Form
	if form.validate_on_submit():
		email = form.email.data
		password = form.password_hash.data
		# Clear the form
		form.email.data = ''
		form.password_hash.data = ''

		# Lookup User By Email Address
		pw_to_check = Users.query.filter_by(email=email).first()
		
		# Check Hashed Password 實務上只要這行就好
		passed = check_password_hash(pw_to_check.password_hash, password)

	return render_template("test_pw.html", 
		email = email,
		password = password,
		pw_to_check = pw_to_check,
		passed = passed,
		form = form)

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
