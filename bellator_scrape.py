import requests
import manage
import untangle
from manage import session
from fight_simulator import database, config, __init__, views
from fight_simulator.database import Fighter

xml = "http://api.spike.com/feeds/bellator/1.0/fighters?key=BELLATORAPPKEY&numberOfItems=188&pageNumber=1"

bellator_f = untangle.parse(xml)
fighters = bellator_f.fighters.fighter

for fighter in fighters:
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
        session.add(fighter)
session.commit()
