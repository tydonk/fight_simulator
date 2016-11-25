import requests
import manage
from manage import session
from fight_simulator import database, config, __init__, views
from fight_simulator.database import User, Fighter, History

import urllib
from urllib.request import urlopen
import xml.etree.ElementTree as etree

response = urllib.request.urlopen("http://api.spike.com/feeds/bellator/1.0/fighters?key=BELLATORAPPKEY&numberOfItems=200&pageNumber=1")
tree = etree.parse(response)
for each in tree:
    print(each)
root = tree.getroot()
for branch in root:
    print(branch)
