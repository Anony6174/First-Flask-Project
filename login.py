from flask import Flask,render_template,request,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///users.db'
app.config["SECRET_KEY"]="2520"
db = SQLAlchemy(app)
app.app_context().push()
reg_value=False

class members(db.Model):
    
    username = db.Column(db.String(200), primary_key=True)
    password = db.Column(db.String(20),nullable=True)
    
    def __repr__(self):
        return f"[ '{self.username}', '{self.password}']"
    
    

@app.route("/register",methods=['POST','GET'])
def register():
    global reg_value
    if request.method == "POST":
        username=request.form["username"]
        password=request.form["password"]
        user1=members.query.filter_by(username=username).first()
        if user1:
            flash("username already exist!!")
            return redirect(url_for('register'))
        user=members(username=username,password=password)
        
        db.session.add(user)
        db.session.commit()
        reg_value = True
        login_user=members.username
        return render_template('index.html',username=login_user)
    elif request.method == "GET":
        return render_template("register.html")
    
@app.route("/login",methods=["POST","GET"])
def login():
    if request.method == "POST":
        if reg_value:
            username = request.form["username"]
            password = request.form["password"]
            if username == members.query.filter_by(username = username).first() and password == members.query.filter_by(password = password).first():
                return render_template("success.html")
            else:
                return render_template("wrong_credentials.html")
            
        else:
            return render_template("first_register.html")
        
    elif request.method == "GET":
        return render_template("login.html")

@app.route("/")
def index():
    global reg_value
    
    if reg_value:
        return redirect(url_for("login"))
    elif not reg_value:
        return redirect(url_for("register"))

if __name__=="__main__":
    app.run(debug=True)



