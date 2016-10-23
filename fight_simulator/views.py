import json
from flask import render_template, request, redirect, url_for, flash, Response
from . import app, decorators
from .database import session, User, Fighter, History
from flask_login import login_required, login_user, current_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from jsonschema import validate, ValidationError

@app.route("/", methods=["GET"])
def welcome():
    return render_template("welcome.html")

@app.route("/howitworks", methods=["GET"])
def how_it_works():
    return render_template("how_it_works.html")   

@app.route("/fight", methods=["GET"])
#@login_required
@decorators.accept("application/json")
def fight():
    data = []
    fighter_data = session.query(Fighter).all()
    #fighter_data = fighter_data[0:10]
    for fighter in fighter_data:
        data.append(fighter.as_dictionary())   
    return Response(render_template("fight.html", 
                    data=data, mimetype="application/json"))

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
        flash("This email address is already in use, please choose another", "danger")
        return redirect(url_for("create_user_get"))
    
    password = request.form["password"]

    if len(password) >= 8:
        user = User(email=email, password=generate_password_hash(password))
        session.add(user)
        session.commit()
        return redirect(url_for("login_get"))
    else:
        flash("Password must be at least 8 characters", "danger")
        return    
         
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("welcome"))

fighter_schema = {
    "properties":{
        "first_name": {"type" : "string"},
        "last_name": {"type" : "string"},
        "nickname": {"type" : "string"},
        "gender": {"type" : "string"},
        "promotion": {"type" : "string"},
        "fighter_image": {"type" : "string"},
        "weight": {"type" : "string"},
        "win": {"type" : "number"},
        "loss": {"type" : "number"},
        "draw": {"type" : "number"},
        },
        "required": [
                    "first_name",
                    "last_name",
                    "gender",
                    "promotion"
                    "weight",
                    "win",
                    "loss",
                    "draw",
                    ]
}
