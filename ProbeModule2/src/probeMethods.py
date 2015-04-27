import queryParams
from flask import Flask, request
import MySQLdb
import requests
import pprint
import urllib
import json
import queries

try:
    conn = MySQLdb.connect(host="localhost", user="root", passwd="HenrietteIda", db="esportrating", charset='utf8', use_unicode=True)
    cursor = conn.cursor()
    
except MySQLdb.Error, e:
    print "Error %d: %s" % (e.args[0], e.args[1])
    sys.exit(1)

#Variables
dataLeague = []
dataMatchHistory = []
dataPerson = []
dataTeamNames = []
dataMatchHistoryPlayers = []


def getLeagueListing():
    response = requests.get(queryParams.endpoint1, params=queryParams.query_params1)
    data = response.json()['result']['leagues']
    for row in data:
        dataLeague.append([row['leagueid'], row['name']])
    return dataLeague

def getMatchHistory(league_id):
    del dataMatchHistory[:]
    query_params2 = { 'key': queryParams.key,
                    'league_id': league_id 
                           }
    response = requests.get(queryParams.endpoint2, params=query_params2)
    data = response.json()['result']['matches']
    for row in data:
        dataMatchHistory.append([row['match_id'], row['radiant_team_id'], row['dire_team_id'], row['players']])
    return dataMatchHistory

def getMatchDetailsPlayers(match_id):
    del dataMatchHistoryPlayers[:]
    query_params3 = { 'key': queryParams.key,
                    'match_id': match_id 
                           }
    response = requests.get(queryParams.endpoint3, params=query_params3)
    data = response.json()['result']['players']
    for row in data:
        dataMatchHistoryPlayers.append([row['account_id'], row['player_slot']])
    return dataMatchHistoryPlayers

def getPlayerSummaries(steam_id):
    del dataPerson[:]
    query_params4 = { 'key': queryParams.key,
        'steamids': steam_id
               } 
    response = requests.get(queryParams.endpoint4, params=query_params4)
    data = response.json()['response']['players']
    for row in data:
        username = 'null' # IKKE ALLE SOM HAR AAPEN PROFIL
        avatar = 'null'
        realname = 'null'
        countrycode = 'null'
        try:
            personaname = data[0]['personaname']
            username = personaname.encode('ascii', 'ignore')
            print "username fra metode: ", username
            try:
                avatar = data[0]['avatarfull']
                print "avatar: ", avatar
            except (KeyError, IndexError): pass
            try:
                realname1 = data[0]['realname']
                realname = realname1.encode('ascii', 'ignore')     
                print "realname: ", realname
            except (KeyError, IndexError): pass
            try:
                countrycode = data[0]['loccountrycode']
            except (KeyError, IndexError): pass
        except (KeyError, IndexError): pass
        
        dataPerson.append([username, avatar, realname, countrycode])
    return dataPerson
    
def insertTeam(team_id, team_name):
    cursor.execute(queries.q3 % (team_id))
    test = cursor.fetchone()[0]
    if test == 0:
        cursor.execute(queries.q4 % (team_id, team_name))
        conn.commit()
        
def getMatchDetails(match_id):
    query_params3 = { 'key': queryParams.key,
                        'match_id': match_id 
                               }
    response = requests.get(queryParams.endpoint3, params=query_params3)
    #data = response.json()['result']['players']
    exists = 0
    try:
        radiant_win = response.json()['result']['radiant_win']
        radiant_id = response.json()['result']['radiant_team_id']
        dire_id = response.json()['result']['dire_team_id']
        start_time = (response.json()['result']['start_time'])
        duration = (response.json()['result']['duration'])
        exists += 1
        print "exists skjer"
    except KeyError: pass
    
def getMatchDetailsTeamName(match_id):
    del dataTeamNames[:]
    query_params3 = { 'key': queryParams.key,
                        'match_id': match_id 
                               }
    response = requests.get(queryParams.endpoint3, params=query_params3)
    radiant_name = 'null'
    dire_name = 'null'
    try:
        radiant_name = response.json()['result']['radiant_name']
        dire_name = response.json()['result']['dire_name']
    except KeyError: pass
    dataTeamNames.append([radiant_name, dire_name])
    return dataTeamNames

def insertPlayer(account_id, username, team_id, avatar, realname, countrycode):
    cursor.execute(queries.q5 % (account_id))
    test = cursor.fetchone()[0]
    if test == 0:
        print 'INSERT INTO Player'
        print username
        cursor.execute(queries.q6 % (account_id, (username + unichr(300)), 1200, 1200, team_id, avatar, realname, countrycode))
        conn.commit()