import json, requests, manage
from manage import session
from fight_simulator import database, config, __init__, views
from fight_simulator.database import User, Fighter, History

response = requests.get("http://ufc-data-api.ufc.com/api/v3/iphone/fighters")
txt = response.text
json.dumps(txt)
fighters = json.loads(txt)

for fighter in fighters:
    if fighter['last_name'] != "TBD":
        if fighter['wins'] != "null":
            if fighter['losses'] != "null":
                if fighter['draws'] != "null":
                    if fighter['weight_class'] != None:
                        fighter = Fighter(
                            first_name=fighter['first_name'], 
                            last_name=fighter['last_name'],
                            nickname=fighter['nickname'],
                            promotion="UFC",
                            fighter_image=fighter['profile_image'],
                            gender = "", 
                            weight=fighter['weight_class'].replace("_", " "), 
                            win=fighter['wins'], 
                            loss=fighter['losses'], 
                            draw=fighter['draws'],
                            )
                        if "Women" in fighter.weight:
                            fighter.gender = "female"
                        else:
                            fighter.gender = "male"                                                        
                        session.add(fighter)
session.commit()