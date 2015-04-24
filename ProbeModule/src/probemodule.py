
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
    





#getLeagueListing    
response = requests.get(queryParams.endpoint1, params=queryParams.query_params1)
data = response.json()['result']['leagues']
datas = []
for u in data:
    datas.append([u['leagueid'], u['name']])

#For loop for every leagueListing
id = datas[1][0]
name = datas[1][1]
cursor.execute("SELECT EXISTS(SELECT id FROM Tournament WHERE tournament_id = '%d')" % (id))
test = cursor.fetchone()[0]
if test == 0:
    cursor.execute("INSERT INTO Tournament (tournament_id, tournament_name) VALUES ('%d', '%s')" % (id, name))
    conn.commit()

matchInfo = []
players = []
#for row in datas:
league_id = id


        
                   
                   
                  



#getMatchHistory
query_params2 = { 'key': queryParams.key,
                'league_id': league_id 
                       }
response = requests.get(queryParams.endpoint2, params=query_params2)
data = response.json()['result']['matches']


for u in data:
    players.append(u['players'])
    matchInfo.append([u['match_id'], u['radiant_team_id'], u['dire_team_id'], u['players']])
for p in matchInfo:
    player_slot = p[3][1]['player_slot']
    account_id = p[3][1]['account_id']
    steam_id = account_id + 76561197960265728
    query_params4 = { 'key': queryParams.key,
    'steamids': steam_id
           } 
    response = requests.get(queryParams.endpoint4, params=query_params4)
    data = response.json()['response']['players']
    pprint.pprint(data)
    # IKKE ALLE SOM HAR AAPEN PROFIL
    username = 'null'
    avatar = 'null'
    realname = 'null'
    countrycode = 'null'
    try:
        username = data[0]['personaname']
        avatar = data[0]['avatarfull']
        realname = data[0]['realname']
        countrycode = data[0]['loccountrycode']
    except KeyError: pass
    match_id = p[0]
    if player_slot < 128:
        team_id = p[2] #for radiant team
        cursor.execute("SELECT EXISTS(SELECT id FROM Team WHERE team_id = '%d')" % (team_id))
        test = cursor.fetchone()[0]
        if test == 0:
            cursor.execute("INSERT INTO Team (team_id, team_name) VALUES ('%d', '%s')" % (team_id, 'null'))
            conn.commit()
    else:
        team_id = p[3]
        cursor.execute("SELECT id FROM Team WHERE team_id = '%d'" % (team_id))
        test = cursor.fetchone()[0]
        if test == 0:
            cursor.execute("INSERT INTO Team (team_id, team_name) VALUES ('%d', '%s')" % (team_id, 'null'))
            conn.commit()
    
    #for row in datas:
    true = 'true'
    query_params3 = { 'key': queryParams.key,
                    'match_id': match_id 
                           }
    response = requests.get(queryParams.endpoint3, params=query_params3)
    #data = response.json()['result']['players']

    radiant_win = response.json()['result']['radiant_win']
    radiant_id = response.json()['result']['radiant_team_id']
    dire_id = response.json()['result']['dire_team_id']
    start_time = (response.json()['result']['start_time'])
    duration = (response.json()['result']['duration'])
    end_time = start_time + duration
  #  league_id = response.json()['result']['leagueid']
    cursor.execute("SELECT EXISTS(SELECT id FROM Matches WHERE match_id = '%d')" % (match_id))
    test = cursor.fetchone()[0]
    if test == 0:
        if radiant_win:
            cursor.execute("INSERT INTO Matches (match_id, tournament_id, winning_team_id, losing_team_id) VALUES ('%d', (SELECT id FROM Tournament WHERE tournament_id = '%d'), '%d', '%d')" % (match_id, league_id, radiant_id, dire_id))
            conn.commit()
        else:
            cursor.execute("INSERT INTO Matches (match_id, tournament_id, winning_team_id, losing_team_id) VALUES ('%d', (SELECT id FROM Tournament WHERE tournament_id = '%d'), '%d', '%d')" % (match_id, league_id, dire_id, radiant_id))
            conn.commit()    
       
       
    print account_id   
    
    cursor.execute("SELECT EXISTS(SELECT id FROM Player WHERE player_id = '%d')" % (account_id))
    test = cursor.fetchone()[0]
    if test == 0:
        print 'IF SKJER'
        cursor.execute("INSERT INTO Player (player_id, username, base_rating, display_rating, team_id, avatar, realname, countrycode) VALUES ('%d', '%s', '%d', '%d', (SELECT id from Team WHERE team_id = '%d'), '%s', '%s', '%s')" % (account_id, username, 1200, 1200, team_id, avatar, realname, countrycode))
        conn.commit()
    
    
    print match_id
    print account_id
    
    cursor.execute("SELECT EXISTS(SELECT * FROM Player_match WHERE match_id = (SELECT id FROM Matches WHERE match_id = '%d') AND player_id = (SELECT id FROM Player WHERE player_id = '%d'))" % (match_id, account_id))
    test = cursor.fetchone()[0]
    
    if test == 0:
        cursor.execute("INSERT INTO Player_match (match_id, player_id, team_id) VALUES ((SELECT id FROM Matches WHERE match_id = '%d'), (SELECT id FROM Player WHERE player_id = '%d'), '%d')" % (match_id, account_id, team_id))
        









