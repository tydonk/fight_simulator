import json
import requests
import manage
import logging
import os
import sys
import time
import untangle
from datetime import datetime
from manage import session
from fight_simulator import database, config, __init__, views
from fight_simulator.database import User, Fighter, History

promo = sys.argv[1].lower()

# UFC scraper
# JSON data from API, some entries need optimization
if promo == 'ufc':
    print('Scraping UFC fighters...')
    time.sleep(3)

    # Set log output file location and log level
    ftime = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
    logging.basicConfig(filename=promo + '_' + ftime + ".log", level=logging.DEBUG)

    response = requests.get("http://ufc-data-api.ufc.com/api/v3/iphone/fighters")
    txt = response.text
    json.dumps(txt)
    fighters = json.loads(txt)
    logging.info("Data request successful, JSON loaded")
    count = 0

    for fighter in fighters:
        try:
            last_name = fighter['last_name']
            first_name = fighter['first_name']
            nickname = fighter['nickname']
            weight = fighter['weight_class']
            promotion = 'UFC'
            gender = ''
            win = fighter['wins']
            loss = fighter['losses']
            draw = fighter['draws']
            fighter_image = fighter['profile_image']
            if all(x != last_name.lower() for x in ('null', 'to be announced',
                                                    'to be determined',
                                                    'tbd', None
                                                    )
                ):
                if all(x != first_name.lower() for x in ('null', 'to be determined',
                                                         '...')
                    ):
                    if fighter['nickname'] != "null":
                        if fighter['wins'] != "null":
                            if fighter['losses'] != "null":
                                if fighter['draws'] != "null":
                                    if fighter['weight_class'] != None:
                                        fighter = Fighter(
                                            first_name = first_name.rstrip(),
                                            last_name = last_name.rstrip(),
                                            nickname = nickname,
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
        except KeyError:
            print('Error adding: ' + first_name + ' ' + last_name)
    session.commit()
    logging.info(str(count) + ' fighters added to DB')
    print(str(count) + ' fighters added to DB')

# Bellator scraper
# XML data from Bellator 'API', some entries need optimization

if promo == 'bellator':
    print('Scraping Bellator fighters...')
    time.sleep(3)

    # Set log output file location and log level
    ftime = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
    logging.basicConfig(filename=promo + '_' + ftime + ".log", level=logging.DEBUG)

    xml = "http://api.spike.com/feeds/bellator/1.0/fighters?key=BELLATORAPPKEY&numberOfItems=188&pageNumber=1"
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
                fighter = Fighter(
                    first_name = fighter.firstName.cdata,
                    last_name = fighter.lastName.cdata,
                    gender = gender,
                    promotion = "Bellator",
                    weight = weight,
                    fighter_image = "/static/images/Body-1.png",
                    win = win,
                    loss = loss,
                    draw = draw,
                    )
                count += 1
                session.add(fighter)
        except KeyError:
            print('Error adding: ' + fighter.firstName.cdata + ' ' + fighter.lastName.cdata)
    session.commit()
    logging.info(str(count) + ' fighters added to DB')
    print(str(count) + ' fighters added to DB')
