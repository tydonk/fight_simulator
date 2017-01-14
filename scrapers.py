import json
import requests
import manage
import logging
import os
import sys
import untangle
from manage import session
from fight_simulator import database, config, __init__, views
from fight_simulator.database import User, Fighter, History
from datetime import datetime

promo = sys.argv[1].lower()

def config_logger():
    # Set log output file location and log level
    ftime = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
    log_name = promo + '_' + ftime
    cwd = os.getcwd() + '/logs/'
    logging.basicConfig(filename=(cwd + log_name + ".log"), level=logging.DEBUG)

# UFC scraper
# JSON data from API, some entries need optimization
if promo == 'ufc':
    print('Scraping UFC fighters...')
    config_logger()

    response = requests.get("http://ufc-data-api.ufc.com/api/v3/iphone/fighters")
    txt = response.text
    json.dumps(txt)
    fighters = json.loads(txt)
    logging.info("Data request successful, JSON loaded")
    count = 0
    entry_count = 0

    for fighter in fighters:
        try:
            entry_count += 1
            nickname = fighter['nickname']
            weight = fighter['weight_class']
            promotion = 'UFC'
            gender = ''
            win = fighter['wins']
            loss = fighter['losses']
            draw = fighter['draws']
            fighter_image = fighter['profile_image']
            if all(x != fighter['last_name'].lower() for x in ('null', 'to be announced',
                                                    'to be determined', 'tbd',
                                                    None
                                                    )
                ):
                if all(x != fighter['first_name'].lower() for x in ('null', 'to be determined',
                                                         '...')
                    ):
                    if (fighter['nickname'] != "null" and
                            fighter['wins'] != "null" and
                            fighter['losses'] != "null" and
                            fighter['draws'] != "null" and
                            fighter['weight_class'] != None):
                                fighter = Fighter(
                                    first_name = fighter['first_name'].rstrip(),
                                    last_name = fighter['last_name'].rstrip(),
                                    nickname = fighter['nickname'],
                                    promotion = promotion,
                                    gender = gender,
                                    weight = weight.replace("_", " "),
                                    win = win,
                                    loss = loss,
                                    draw = draw,
                                    fighter_image = fighter_image,
                                    )
                                if "Women" in fighter.weight:
                                    fighter.gender = "female"
                                    fighter.weight = fighter.weight.split(' ')[1]
                                else:
                                    fighter.gender = "male"
                                count += 1
                                session.add(fighter)
        except (KeyError, AttributeError):
            print(entry_count)
    session.commit()
    logging.info(str(count) + ' fighters added to DB')
    print(str(count) + ' fighters added to DB')

# Bellator scraper
# XML data from Bellator 'API', some entries need optimization
if promo == 'bellator':
    print('Scraping Bellator fighters...')
    config_logger()
    xml = "http://api.spike.com/feeds/bellator/1.0/fighters?key=BELLATORAPPKEY&numberOfItems=500&pageNumber=1"
    logging.info("Data request successful, XML loaded")
    bellator_f = untangle.parse(xml)
    logging.info("XML Untangled")
    fighters = bellator_f.fighters.fighter
    count = 0

    for fighter in fighters:
        try:
            if fighter.firstName != "To Be Announced":
                record = fighter.record.cdata
                win = record.split('-')[0]
                loss = record.split('-')[1]
                draw = record.split('-')[2]
                if fighter.sex.cdata == 'W':
                    gender = 'female'
                else:
                    gender = 'male'
                fweight = float(fighter.weight.cdata)
                if fweight <= 126:
                    weight = "Flyweight"
                if 127 <= fweight <= 136:
                    weight = "Bantamweight"
                if 137 <= fweight <= 146:
                    weight = "Featherweight"
                if 147 <= fweight <= 156:
                    weight = "Lightweight"
                if 157 <= fweight <= 171:
                    weight = "Welterweight"
                if 172 <= fweight <= 186:
                    weight = "Middleweight"
                if 187 <= fweight <= 206:
                    weight = "Light Heavyweight"
                if 207 <= fweight:
                    weight = "Heavyweight"
                try:
                    height = fighter.height.cdata
                    height = (int(height[0]) * 12) + int(height[2:])
                except IndexError:
                    height = None
                try:
                    dob = fighter.dob.cdata
                except IndexError:
                    dob = None
                fighter = Fighter(
                    first_name = fighter.firstName.cdata,
                    last_name = fighter.lastName.cdata,
                    dob = dob,
                    gender = gender,
                    promotion = "Bellator",
                    weight = weight,
                    fighter_image = "/static/images/Body-1.png",
                    win = win,
                    loss = loss,
                    draw = draw,
                    height = height,
                    )
                session.add(fighter)
                count += 1
        except IndexError as inst:
            print('Error adding: ' + fighter.firstName.cdata + ' ' + fighter.lastName.cdata)
            print(type(inst), inst)
    session.commit()
    logging.info(str(count) + ' fighters added to DB')
    print(str(count) + ' fighters added to DB')
