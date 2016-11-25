import json
import requests
import manage
from manage import session
from fight_simulator import database, config, __init__, views
from fight_simulator.database import User, Fighter, History

response = requests.get("http://ufc-data-api.ufc.com/api/v3/iphone/fighters")
txt = response.text
json.dumps(txt)
fighters = json.loads(txt)

for fighter in fighters:
    if (
        fighter['last_name'] != None and
        fighter['last_name'] != "null" and
        fighter['last_name'] != "To Be Determined" and
        fighter['last_name'] != "To be determined" and
        fighter['last_name'] != "To Be Announced" and
        fighter['last_name'] != "To be announced" and
        fighter['last_name'] != "TBD"
        ):
        if (
            fighter['first_name'] != "null" and
            fighter['first_name'] != "To be determined..." and
            fighter['first_name'] != "..."
            ):
            if fighter['nickname'] != "null":
                if fighter['wins'] != "null":
                    if fighter['losses'] != "null":
                        if fighter['draws'] != "null":
                            if fighter['weight_class'] != None:
                                if 'profile_image' in fighter:
                                    fighter = Fighter(
                                        first_name=fighter['first_name'].rstrip(),
                                        last_name=fighter['last_name'],
                                        nickname=fighter['nickname'],
                                        promotion="UFC",
                                        gender = "",
                                        weight=fighter['weight_class'].replace("_", " "),
                                        win=fighter['wins'],
                                        loss=fighter['losses'],
                                        draw=fighter['draws'],
                                        fighter_image=fighter['profile_image'],
                                        )
                                    if "Women" in fighter.weight:
                                        fighter.gender = "female"
                                        fighter.weight = fighter.weight.split(' ')[1]
                                    else:
                                        fighter.gender = "male"
                                    session.add(fighter)
session.commit()
