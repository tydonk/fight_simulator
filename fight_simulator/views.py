from flask import render_template, request, redirect, url_for, flash
from . import app, decorators
from .database import session, User, Fighter, History
from flask_login import login_required, login_user, current_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from getpass import getpass

'''fighter_schema = {
    "properties":{
        "first_name": {"type" : "string"},
        "last_name": {"type" : "string"},
        "weight": {"type" : "string"},
        "win": {"type" : "number"},
        "loss": {"type" : "number"},
        "draw": {"type" : "number"},
        }
        "required": [
                    "first_name",
                    "last_name",
                    "weight",
                    "win",
                    "loss",
                    "draw",
                    ]
}'''

@app.route("/")
def welcome():
    return render_template("welcome.html")

@app.route("/fight", methods=["GET"])
#@login_required
def fight():
    fighter_data = session.query(Fighter)
    fighter_data = fighter_data.order_by(Fighter.last_name.asc())
    count = session.query(Fighter).count()
    for fighter in fighter_data:
        first_name = fighter.first_name
        last_name = fighter.last_name
        win = fighter.win
        loss = fighter.loss
        draw = fighter.draw
        weight = fighter.weight       
    return render_template("fight.html", 
                    fighter_data=fighter_data, 
                    first_name=first_name, 
                    last_name=last_name,
                    win = win,
                    loss = loss,
                    draw = draw,
                    weight = weight,
                    count=count
                    )

@app.route("/login", methods=["GET"])
def login_get():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login_post():
    email = request.form["email"]
    password = request.form["password"]
    user = session.query(User).filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        flash("Incorrect username or password", "danger")
        return redirect(url_for("login_get"))
    
    login_user(user)
    return redirect(request.args.get('next') or url_for("fight"))

@app.route("/create_user", methods=["GET"])
def create_user_get():
    return render_template("create_user.html")

@app.route("/create_user", methods=["POST"])
def create_user_post():
    email = request.form["email"]
    if session.query(User).filter_by(email=email).first():
        flash("User with that email address already exists", "danger")
        return 
    
    password = request.form["password"]

    if len(password) >= 8:
        user = User(email=email, password=generate_password_hash(password))
        session.add(user)
        session.commit()
        flash("User created")
        return redirect(url_for("login_get"))
    else:
        flash("Password must be at least 8 characters", "danger")
        return    
         
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("welcome"))
