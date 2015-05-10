
from flask import Flask, request
import MySQLdb
import requests
import pprint
import urllib
import json
import queryParams

try:
    conn = MySQLdb.connect(host="localhost", user="root", passwd="HenrietteIda", db="esportrating")
    cursor = conn.cursor()
    
except MySQLdb.Error, e:
    print "Error %d: %s" % (e.args[0], e.args[1])
    sys.exit(1)
    

steam_id = 76561198011724846
query_params4 = { 'key': queryParams.key,
             'steamids': steam_id
                    } 
response = requests.get(queryParams.endpoint4, params=query_params4)
data = response.json()['response']['players']
username = data[3]
print username

/home/henriette/Bachelor/ProbeModule/testing.py