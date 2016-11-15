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
from .login import login_manager

@app.route("/", methods=["GET"])
def welcome():
    return render_template("welcome.html")

@app.route("/howitworks", methods=["GET"])
def how_it_works():
    return render_template("how_it_works.html")

@app.route("/fight", methods=["GET"])
@decorators.accept("application/json")
def fight():
    data = []
    # get fighters from database
    fighter_data = session.query(Fighter).all()
    fighter_data = fighter_data[0:99]
    # append them to data array in dictionary form
    for fighter in fighter_data:
        data.append(fighter.as_dictionary())
    # alphabetize fighters
    data = sorted(data, key=lambda k: k['last_name'])
    return Response(render_template("new_fight.html",
                    data=data, mimetype="application/json"))

@app.route("/fight", methods=["GET", "POST"])
@decorators.accept("application/json")
#@decorators.require("application/json")
def return_results():
    data = []
    fighter_data = session.query(Fighter).all()
    fighter_data = fighter_data[0:99]
    for fighter in fighter_data:
        data.append(fighter.as_dictionary())

    now = datetime.now()
    year = now.year
    month = now.month
    day = now.day
    current_date = '{}/{}/{}'.format(month, day, year)

    # get matched fighters from client
    red_gender = request.form['red_gender']
    red_fighter_req = request.form['red_fighter']
    blue_gender = request.form['blue_gender']
    blue_fighter_req = request.form['blue_fighter']

    # match fighters to database to access properties
    for fighter in fighter_data:
        full_name = fighter.last_name + ", " + fighter.first_name
        if (full_name == red_fighter_req):
            red_fighter = fighter
            red_record = [fighter.win, fighter.loss, fighter.draw]
            red_win_perc = (red_record[0] + \
                (red_record[1] * .5)) / \
                (red_record[0] + red_record[1] + red_record[2]) * 100
            red_win_perc = round(red_win_perc)

        if (full_name == blue_fighter_req):
            blue_fighter = fighter
            blue_record = [fighter.win, fighter.loss, fighter.draw]
            blue_win_perc = (blue_record[0] + \
                (blue_record[1] * .5)) / \
                (blue_record[0] + blue_record[1] + blue_record[2]) * 100
            blue_win_perc = round(blue_win_perc)

    # determine a winner based on win %
    if red_win_perc > blue_win_perc:
        winner = red_fighter_req
    # Prevent draw by selecting random fighter is win % is equal
    elif red_win_perc == blue_win_perc:
        combatants = [red_fighter_req, blue_fighter_req]
        winner = random.choice(combatants)
    else:
        winner = blue_fighter_req

    # list of outcomes and submissions for random results
    outcomes = ["Knockout", "Technical Knockout", "Submission",
			"Doctor Stoppage", "Unanimous Decision",
			"Split Decision", "Majority Decision"]

    submissions = ["arm triangle", "triangle", "rear naked choke", "guillotine",
        "gogoplata", "arm bar", "kimura", "americana", "omoplata", "knee bar",
        "ankle lock", "heel hook", "toe hold", "can opener", "twister",
        "achilles lock", "bicep slicer", "leg slicer"]

    # generate random round and time
    end_round = randint(1,3)
    minute = randint(0,4)
    second_1 = randint(0,5)
    second_2 = randint(1,9)
    end_time = "{}:{}{}".format(minute, second_1, second_2)

    # generate random result method and account for specific results
    method = random.choice(outcomes)
    if method == "Submission":
        method = method + " ({})".format(random.choice(submissions))
    elif len(method.split(" ")) == 2:
        if (method.split(" ")[1]) == "Decision":
            end_round = "3"
            end_time = "5:00"

    red_fighter = red_fighter.as_dictionary()
    blue_fighter = blue_fighter.as_dictionary()

    # load results in dictionary form
    results = [{'winner': winner,
                'end_round': end_round,
                'end_time': end_time,
                'method': method,
                'blue_fighter': blue_fighter,
                'red_fighter': red_fighter,
                }]

    # add fight results to user
    # history if user is logged in
    if current_user.is_authenticated:
        history_entry = History(
            fight_date=current_date,
            has_occured=True,
            red_corner=red_fighter_req,
            blue_corner=blue_fighter_req,
            winner=winner,
            end_round=end_round,
            end_time=end_time,
            method=method,
            user_id=current_user.id)

        session.add(history_entry)
        session.commit()

    return Response(render_template("results.html",
                    data=data, results=results, mimetype="application/json"))

@app.route("/user_history", methods=["GET"])
@login_required
@decorators.accept("application/json")
def user_history():
    user_history = []
    user_id = current_user.id
    history = session.query(History).filter(History.user_id == user_id).all()
    user_history = json.dumps([fight.as_dictionary() for fight in history])
    return Response(render_template("user_history.html",
                    user_history=user_history, mimetype="application/json"))

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
        return redirect(url_for("create_user_post"))

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

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("welcome"))
