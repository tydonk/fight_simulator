import json
import random

from flask import render_template, request, redirect, url_for, flash, Response
from . import app, decorators
from .database import session, User, Fighter, History
from flask_login import login_required, login_user, current_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from jsonschema import validate, ValidationError
from datetime import datetime
from random import randint
from .login import login_manager

@app.route("/")
def welcome():
    return render_template("welcome.html")

@app.route("/howitworks", methods=["GET"])
def how_it_works():
    return render_template("how_it_works.html")

@app.route("/fight", methods=["GET"])
def fight():
    return render_template("fight.html")

@app.route("/fight", methods=["POST"])
@decorators.accept("application/json")
def return_results():
    def get_fighter_record(fighter):
        """Return fighter record for calculating win percentage."""
        record = [fighter.win, fighter.loss, fighter.draw]
        return record

    def calc_win_perc(record):
        """Calculate fighter win percentage based on record."""
        wins = record[0]
        losses = record[1]
        draws = record[2]
        win_percent = round((wins+(draws*.5))/(wins+losses+draws)*100)
        return win_percent

    def weight_multiplier(fighter):
        """Return weight multiplier for fighter.

        To account for weight discrepencies, fighters who are 2 or more weight
        classes above their opponent will receive a bonus, based on the
        following chart:

        Classes apart| Bonus amount
        ---------------------------
            <=1      | no bonus
            2-3      | +5
            4-5      | +10
            6-7      | +15
        """

        mp = [
            'Strawweight','Flyweight','Bantamweight','Featherweight',
            'Lightweight','Welterweight','Middleweight','Light Heavyweight',
            'Heavyweight'
        ]

        weight_multi = mp.index(fighter.weight) + 1
        return weight_multi

    def calc_new_win_perc(fighter):
        """Return win percentage using fighter record and user history."""
        name = fighter.last_name + ", " + fighter.first_name
        winners = []
        losers = []
        history_all = session.query(History).filter(
                History.user_id == current_user.id).all()
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

    """Get current date."""
    now = datetime.now()
    year = now.year
    month = now.month
    day = now.day
    current_date = '{}/{}/{}'.format(month, day, year)

    # List of outcomes and submissions for generating random results
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

    # Generate random round and time for fight results
    rnd_req = request.form['rounds']
    rnd_req = int(rnd_req)
    end_round = randint(1,rnd_req)
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
            end_round = rnd_req
            end_time = "5:00"

    # Get matched fighters from client
    red_fighter_req = request.form['red_name']
    blue_fighter_req = request.form['blue_name']

    # Get fighters from database
    data = []
    fighter_data = session.query(Fighter).all()
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

    # Apply bonus based on weight classes.
    # Then determine a winner based on win %.
    # Prevent draw by selecting random fighter is win % is equal.

    red_mp = weight_multiplier(red_fighter)
    blue_mp = weight_multiplier(blue_fighter)
    mp_diff = red_mp - blue_mp

    if 2 <= mp_diff <= 3:
        red_mp = 5
    elif 4 <= mp_diff <= 5:
        red_mp = 10
    elif 6 <= mp_diff <=7:
        red_mp = 15
    else:
        red_mp = 0

    if (-3 <= mp_diff <= -2):
        blue_mp = 5
    elif (-5 <= mp_diff <= -4):
        blue_mp = 10
    elif (-7 <= mp_diff <= -6):
        blue_mp = 15
    else:
        blue_mp = 0

    red_total = red_win_perc + red_mp
    blue_total = blue_win_perc + blue_mp

    if red_total > blue_total:
        winner = red_fighter_req
    elif red_total == blue_total:
        combatants = [red_fighter_req, blue_fighter_req]
        winner = random.choice(combatants)
    else:
        winner = blue_fighter_req

    red_fighter = red_fighter.as_dictionary()
    blue_fighter = blue_fighter.as_dictionary()

    # Load results in dictionary form
    result = [
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
                    results=result, mimetype="application/json"), 201)

@app.route("/user_history", methods=["GET"])
@app.route("/user_history/<int:page>")
@login_required
@decorators.accept("application/json")
def user_history(page=1):
    paginate_by = 20
    user_id = current_user.id

    # Zero-indexed page
    page_index = page - 1
    count = session.query(History).filter(History.user_id == user_id).count()
    start = page_index * paginate_by
    end = start + paginate_by
    total_pages = (count - 1) // paginate_by + 1
    has_next = page_index < total_pages - 1
    has_prev = page_index > 0

    history = session.query(History).filter(History.user_id == user_id).all()
    user_history = []

    for fight in history:
        if fight.visible == True:
            user_history.append(fight.as_dictionary())

    user_history = user_history[start:end]

    return Response(render_template("user_history.html",
        user_history=user_history,
        page=page,
        has_next=has_next,
        has_prev=has_prev,
        total_pages=total_pages,
        count=count,
        mimetype="application/json"), 200)

@app.route("/user_history", methods=["POST"])
@login_required
def clear_history():
    """Change entries to invisible """
    user_id = current_user.id
    history = session.query(History).filter(History.user_id == user_id).all()
    for each in history:
        each.visible = False
    session.commit()
    return redirect(url_for("user_history"))

@app.route("/create_user", methods=["GET"])
def create_user_get():
    """Return registration page."""
    return render_template("create_user.html")

@app.route("/create_user", methods=["POST"])
def create_user_post():
    """Commit user credentials to database if they don't already exist."""
    email = request.form["email"]
    if session.query(User).filter_by(email=email).first():
        flash("This email address is already in use, please choose another",
              "danger"
        )
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
    """Return login page."""
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login_post():
    """Log user in if credentials match database."""
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
    """Logout current user."""
    logout_user()
    return redirect(url_for("welcome"))

"""API endpoints."""
@app.route("/api/fighters", methods=["GET"])
@decorators.accept("application/json")
def fighters_all():
    """Return all fighters."""
    fighters = session.query(Fighter).all()
    data = [fighter.as_dictionary() for fighter in fighters]
    data = sorted(data, key=lambda k: k['last_name'])
    data = json.dumps(data)
    return Response(data, 200, mimetype="application/json")

@app.route("/api/fighter/<int:id>/", methods=["GET"])
@decorators.accept("application/json")
def fighter_by_id(id):
    """Return a fighter by their id."""
    fighters = session.query(Fighter).filter(Fighter.id == id).all()
    data = json.dumps([fighter.as_dictionary() for fighter in fighters])
    return Response(data, 200, mimetype="application/json")

@app.route("/api/fighter/name/<last_name>/<first_name>/", methods=["GET"])
@decorators.accept("application/json")
def fighter_by_name(last_name, first_name):
    """Return a fighter by their full name."""
    fighters = session.query(Fighter).filter(Fighter.last_name == last_name,
            Fighter.first_name == first_name).all()
    data = json.dumps([fighter.as_dictionary() for fighter in fighters])
    return Response(data, 200, mimetype="application/json")

@app.route("/api/fighters/<gender>/", methods=["GET"])
@decorators.accept("application/json")
def fighters_by_gender(gender):
    """Return fighters by gender."""
    fighters = session.query(Fighter).filter(Fighter.gender == gender).all()
    data = [fighter.as_dictionary() for fighter in fighters]
    data = sorted(data, key=lambda k: k['last_name'])
    data = json.dumps(data)
    return Response(data, 200, mimetype="application/json")

@app.route("/api/fighters/<gender>/<promotion>/", methods=["GET"])
@decorators.accept("application/json")
def fighters_gender_promotion(gender, promotion):
    """Return fighters by gender and promotion."""
    fighters = session.query(Fighter).filter(Fighter.gender == gender,
            Fighter.promotion == promotion).all()
    data = [fighter.as_dictionary() for fighter in fighters]
    data = sorted(data, key=lambda k: k['last_name'])
    data = json.dumps(data)
    return Response(data, 200, mimetype="application/json")

@app.route("/api/fighters/<gender>/<promotion>/<weight>/", methods=["GET"])
@decorators.accept("application/json")
def fighters_gender_promotion_weight(gender, promotion, weight):
    """Return fighters by gender, promotion and weight."""
    fighters = session.query(Fighter).filter(Fighter.gender == gender,
                                             Fighter.promotion == promotion,
                                             Fighter.weight == weight
                                             )
    data = [fighter.as_dictionary() for fighter in fighters]
    data = sorted(data, key=lambda k: k['last_name'])
    data = json.dumps(data)
    return Response(data, 200, mimetype="application/json")
