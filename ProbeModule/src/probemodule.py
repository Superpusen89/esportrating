
from flask import Flask, request
import MySQLdb
import requests
import pprint
import urllib
import json

try:
    conn = MySQLdb.connect(host="localhost", user="root", passwd="HenrietteIda", db="esportrating")
    cursor = conn.cursor()
    
except MySQLdb.Error, e:
    print "Error %d: %s" % (e.args[0], e.args[1])
    sys.exit(1)
    
query_params = { 'key': 'C60B2F253D948B27317D3EE293EE04ED',
                'match_id': '992769598' 
		       }

endpoint = 'http://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/v0001/'
    
response = requests.get(endpoint, params=query_params)
url = response.url
print url
data = response.json()['result']['radiant_win']
pprint.pprint(data)
