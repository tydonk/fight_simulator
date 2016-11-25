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
    # Get fighters from database
    fighter_data = session.query(Fighter).all()
    #fighter_data = fighter_data[0:99]
    # Append them to data array in dictionary form
    for fighter in fighter_data:
        data.append(fighter.as_dictionary())
    # Alphabetize fighters
    data = sorted(data, key=lambda k: k['last_name'])
    return Response(render_template("new_fight.html",
                    data=data, mimetype="application/json"))

@app.route("/fight", methods=["GET", "POST"])
@decorators.accept("application/json")
def return_results():

    def get_fighter_record(fighter):
        record = [fighter.win, fighter.loss, fighter.draw]
        return record

    def calc_win_perc(record):
        win_percent = (record[0] + (record[2] * .5)) / (record[0] + record[1] + record[2]) * 100
        win_percent = round(win_percent)
        return win_percent

    def calc_new_win_perc(fighter):
        name = fighter.last_name + ", " + fighter.first_name
        winners = []
        losers = []
        history_all = session.query(History).filter(History.user_id == current_user.id).all()
        for each in history_all:
            if each.blue_corner == each.winner:
                winners.append(each.blue_corner)
                losers.append(each.red_corner)
            else:
                losers.append(each.blue_corner)
                winners.append(each.red_corner)
        if name in winners:
            win_count = winners.count(name)
        else:
            win_count = 0
        if name in losers:
            loss_count = losers.count(name)
        else:
            loss_count = 0
        win = fighter.win + win_count
        loss = fighter.loss + loss_count
        new_record = [win, loss, fighter.draw]
        new_win_perc = calc_win_perc(new_record)
        return new_win_perc

    # Get current date
    now = datetime.now()
    year = now.year
    month = now.month
    day = now.day
    current_date = '{}/{}/{}'.format(month, day, year)

    # List of outcomes and submissions for random results
    outcomes = [
        "Knockout", "Technical Knockout", "Submission",
		"Doctor Stoppage", "Unanimous Decision",
		"Split Decision", "Majority Decision"
    ]

    submissions = [
        "arm triangle", "triangle", "rear naked choke", "guillotine",
        "gogoplata", "arm bar", "kimura", "americana", "omoplata",
        "knee bar", "ankle lock", "heel hook", "toe hold", "can opener",
        "twister", "achilles lock", "bicep slicer", "leg slicer"
    ]

    # Generate random round and time
    end_round = randint(1,3)
    minute = randint(0,4)
    second_1 = randint(0,5)
    second_2 = randint(1,9)
    end_time = "{}:{}{}".format(minute, second_1, second_2)

    # Generate random result method and account for specific results
    method = random.choice(outcomes)
    if method == "Submission":
        method = method + " ({})".format(random.choice(submissions))
    elif len(method.split(" ")) == 2:
        if (method.split(" ")[1]) == "Decision":
            end_round = "3"
            end_time = "5:00"

    # Get matched fighters from client
    red_fighter_req = request.form['red_name']
    blue_fighter_req = request.form['blue_name']

    # Get fighters from database
    data = []
    fighter_data = session.query(Fighter).all()
    # = fighter_data[0:99]
    for fighter in fighter_data:
        data.append(fighter.as_dictionary())

    # Match fighters to database to access properties
    for fighter in fighter_data:
        full_name = fighter.last_name + ", " + fighter.first_name
        if full_name == red_fighter_req:
            red_fighter = fighter
            if current_user.is_authenticated:
                red_win_perc = calc_new_win_perc(red_fighter)
            else:
                red_record = get_fighter_record(red_fighter)
                red_win_perc = calc_win_perc(red_record)

        if full_name == blue_fighter_req:
            blue_fighter = fighter
            if current_user.is_authenticated:
                blue_win_perc = calc_new_win_perc(blue_fighter)
            else:
                blue_record = get_fighter_record(blue_fighter)
                blue_win_perc = calc_win_perc(blue_record)

    # Determine a winner based on win %
    if red_win_perc > blue_win_perc:
        winner = red_fighter_req
    # Prevent draw by selecting random fighter is win % is equal
    elif red_win_perc == blue_win_perc:
        combatants = [red_fighter_req, blue_fighter_req]
        winner = random.choice(combatants)
    else:
        winner = blue_fighter_req

    red_fighter = red_fighter.as_dictionary()
    blue_fighter = blue_fighter.as_dictionary()

    # Load results in dictionary form
    results = [
        {'winner': winner,
        'end_round': end_round,
        'end_time': end_time,
        'method': method,
        'blue_fighter': blue_fighter,
        'red_fighter': red_fighter
        }
    ]

    # Add fight results to user history if user is logged in
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
            user_id=current_user.id,
            visible=True,
        )

        session.add(history_entry)
        session.commit()

    return Response(render_template("results.html",
                    data=data, results=results, mimetype="application/json"))

@app.route("/api/fighters", methods=["GET"])
@decorators.accept("application/json")
def fighters_all():
    ''' Return all fighters '''
    fighters = session.query(Fighter).all()
    data = [fighter.as_dictionary() for fighter in fighters]
    data = sorted(data, key=lambda k: k['last_name'])
    data = json.dumps(data)
    return Response(data, mimetype="application/json")

@app.route("/api/fighters/<int:id>/", methods=["GET"])
@decorators.accept("application/json")
def fighter_by_id(id):
    ''' Return fighter by id '''
    fighters = session.query(Fighter).filter(Fighter.id == id).all()
    data = json.dumps([fighter.as_dictionary() for fighter in fighters])
    return Response(data, mimetype="application/json")

@app.route("/api/fighters/name/<last_name>/<first_name>/", methods=["GET"])
@decorators.accept("application/json")
def fighter_by_name(last_name, first_name):
    ''' Return fighter by name '''
    fighters = session.query(Fighter).filter(Fighter.last_name == last_name,
                                             Fighter.first_name == first_name).all()
    data = json.dumps([fighter.as_dictionary() for fighter in fighters])
    return Response(data, mimetype="application/json")

@app.route("/api/fighters/<gender>/", methods=["GET"])
@decorators.accept("application/json")
def fighters_by_gender(gender):
    ''' Return fighters by gender '''
    fighters = session.query(Fighter).filter(Fighter.gender == gender).all()
    data = [fighter.as_dictionary() for fighter in fighters]
    data = sorted(data, key=lambda k: k['last_name'])
    data = json.dumps(data)
    return Response(data, mimetype="application/json")

@app.route("/api/fighters/<gender>/<promotion>/", methods=["GET"])
@decorators.accept("application/json")
def fighters_gender_promotion(gender, promotion):
    ''' Return fighters by gender and promotion '''
    fighters = session.query(Fighter).filter(Fighter.gender == gender, Fighter.promotion == promotion).all()
    data = [fighter.as_dictionary() for fighter in fighters]
    data = sorted(data, key=lambda k: k['last_name'])
    data = json.dumps(data)
    return Response(data, mimetype="application/json")

@app.route("/api/fighters/<gender>/<promotion>/<weight>/", methods=["GET"])
@decorators.accept("application/json")
def fighters_gender_promotion_weight(gender, promotion, weight):
    ''' Return fighters by gender, promotion and weight '''
    fighters = session.query(Fighter).filter(Fighter.gender == gender,
                                             Fighter.promotion == promotion,
                                             Fighter.weight == weight
                                             )
    data = [fighter.as_dictionary() for fighter in fighters]
    data = sorted(data, key=lambda k: k['last_name'])
    data = json.dumps(data)
    return Response(data, mimetype="application/json")

@app.route("/user_history", methods=["GET"])
@login_required
@decorators.accept("application/json")
def user_history():
    user_history = []
    user_id = current_user.id
    history = session.query(History).filter(History.user_id == user_id).all()
    user_history = []
    for fight in history:
        if fight.visible == True:
            user_history.append(fight.as_dictionary())
    return Response(render_template("user_history.html",
        user_history=user_history, mimetype="application/json"))

@app.route("/user_history", methods=["POST"])
@login_required
def clear_history():
    user_id = current_user.id
    history = session.query(History).filter(History.user_id == user_id).all()
    for each in history:
        each.visible = False
    session.commit()
    return redirect(url_for("user_history"))

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
