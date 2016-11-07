import json
from flask import render_template, request, redirect, url_for, flash, Response
from . import app, decorators
from .database import session, User, Fighter, History
from flask_login import login_required, login_user, current_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from jsonschema import validate, ValidationError
from datetime import datetime
from random import randint
import random

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
    fighter_data = fighter_data[0:99]
    for fighter in fighter_data:
        data.append(fighter.as_dictionary())
    data = sorted(data, key=lambda k: k['last_name'])
    return Response(render_template("new_fight.html",
                    data=data, mimetype="application/json"))

@app.route("/fight", methods=["POST"])
#@login_required
#@decorators.accept("application/json")
#@decorators.require("application/json")
def return_results():
    now = datetime.now()
    year = now.year
    month = now.month
    day = now.day
    current_date = '{}/{}/{}'.format(month, day, year)

    fighter_data = session.query(Fighter).all()
    fighter_data = fighter_data[0:99]
    red_gender = request.form['red_gender']
    red_fighter = request.form['red_fighter']
    blue_gender = request.form['blue_gender']
    blue_fighter = request.form['blue_fighter']

    if red_fighter == blue_fighter:
        print("that's a no-no!")

    for fighter in fighter_data:
        full_name = fighter.last_name + ", " + fighter.first_name
        if (full_name == red_fighter):
            red_record = [fighter.win, fighter.loss, fighter.draw]
            red_win_perc = (red_record[0] + \
                (red_record[1] * .5)) / \
                (red_record[0] + red_record[1] + red_record[2]) * 100
            red_win_perc = round(red_win_perc)

        if (full_name == blue_fighter):
            blue_record = [fighter.win, fighter.loss, fighter.draw]
            blue_win_perc = (blue_record[0] + \
                (blue_record[1] * .5)) / \
                (blue_record[0] + blue_record[1] + blue_record[2]) * 100
            blue_win_perc = round(blue_win_perc)

    if red_win_perc > blue_win_perc:
        winner = red_fighter
    elif red_win_perc == blue_win_perc:
        print("DRAW")
    else:
        winner = blue_fighter

    outcomes = ["Knockout", "Technical Knockout", "Submission",
			"Doctor Stoppage", "Unanimous Decision",
			"Split Decision", "Majority Decision"]

    submissions = ["arm triangle", "triangle", "rear naked choke", "guillotine",
        "gogoplata", "arm bar", "kimura", "americana", "omoplata", "knee bar",
        "ankle lock", "heel hook", "toe hold", "can opener", "twister",
        "achilles lock", "bicep slicer", "leg slicer"]

    method = random.choice(outcomes)
    if method == "Submission":
        method = method + " ({})".format(random.choice(submissions))

    end_round = randint(1,3)
    minute = randint(0,4)
    second_1 = randint(0,5)
    second_2 = randint(1,9)
    end_time = "{}:{}{}".format(minute, second_1, second_2)

    #new_fighter = History(fight_date=current_date, has_occured=true,
    #red_corner=red_fighter, blue_corner=blue_fighter, winner=red_fighter,
    #end_round=end_round, end_time=end_time, method=method

    return redirect(url_for("fight"))

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
