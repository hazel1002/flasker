from crypt import methods
import email
from email.policy import default
from flask import Flask, flash, render_template, request
from flask_wtf import FlaskForm
from importlib_metadata import method_cache
from sqlalchemy import null
from wtforms import StringField, SubmitField, EmailField, IntegerField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


# Create a Flask Instance
app = Flask(__name__)
# Add MYSQL Database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:12345678@localhost:3306/user"
# SECRET KEY!
app.config['SECRET_KEY'] = "my super secret key that is no one is supposed to know" #create secret key
# Initialize The Database
db = SQLAlchemy(app)




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
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

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
    submit = SubmitField("Submit")

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
        try:
            db.session.commit()
            flash("User Updated Successfully!")
            return render_template("update.html", form=form, name_to_update=name_to_update)
        except:
            flash("Error! Looks like there was a problem...try again!")
            return render_template("update.html", form=form, name_to_update=name_to_update)
    else:
        return render_template("update.html", form=form, name_to_update=name_to_update)






# def index():
#     return "<h1>Hello World</h1>"

@app.route('/user/add',methods=['GET','POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(username=form.name.data, bankername=form.bankername.data,
            gender=form.gender.data, userage=form.userage.data, phonenumber=form.phonenumber.data, email=form.email.data, loantype=form.loantype.data, loanAMT=form.loanAMT.data )
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.bankername.data = ''
        form.gender.data = ''
        form.userage.data = ''
        form.phonenumber.dat = ''
        form.email.data = ''
        form.loantype.data = ''
        form.loanAMT.data = ''
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


