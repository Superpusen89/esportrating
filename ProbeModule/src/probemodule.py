# -*- coding: utf-8 -*-

from flask import Flask, request
import MySQLdb
import requests
import pprint
import urllib
import json
import queryParams
import time

try:
    conn = MySQLdb.connect(host="localhost", user="root", passwd="HenrietteIda", db="esportrating", use_unicode=True, charset='utf8')
    cursor = conn.cursor()
    
except MySQLdb.Error, e:
    print "Error %d: %s" % (e.args[0], e.args[1])
    sys.exit(1)
    

#Variables
matchInfo = []
players = []
datas = []


#getLeagueListing    
response = requests.get(queryParams.endpoint1, params=queryParams.query_params1)
data = response.json()['result']['leagues']
for u in data:
    datas.append([u['leagueid'], u['name']])
#For loop for every leagueListing
for row in datas:
    print "for loop - leagueListing"
    league_id = row[0]
    league_name = row[1]
    print league_name
    cursor.execute("SELECT EXISTS(SELECT id FROM Tournament WHERE tournament_id = '%d')" % (league_id))
    test = cursor.fetchone()[0]
    if test == 0:
        print "INSERT INTO Tournament"
        cursor.execute("INSERT INTO Tournament (tournament_id, tournament_name) VALUES ('%d', '%s')" % (league_id, league_name))
        conn.commit()

    #getMatchHistory for each leage_id
    query_params2 = { 'key': queryParams.key,
                    'league_id': id 
                           }
    response = requests.get(queryParams.endpoint2, params=query_params2)
    response.url
    data = response.json()['result']['matches']
    for u in data: # MULIG DENNE IKKE ER NODVENDIG?
        del matchInfo[:]
        players.append(u['players'])
        matchInfo.append([u['match_id'], u['radiant_team_id'], u['dire_team_id'], u['players']])
    for p in matchInfo:
        player_slot = p[3][1]['player_slot']
        account_id = p[3][0]['account_id']
        
        steam_id = account_id + 76561197960265728
        #getPlayerSummaries
        query_params4 = { 'key': queryParams.key,
        'steamids': steam_id
               } 
        response = requests.get(queryParams.endpoint4, params=query_params4)
        data = response.json()['response']['players']
        username = 'null' # IKKE ALLE SOM HAR AAPEN PROFIL
        avatar = 'null'
        realname = 'null'
        countrycode = 'null'
        try:
            personaname = data[0]['personaname']
            username = personaname.encode('ascii', 'ignore')
        except (KeyError, IndexError): pass
        try:
            avatar = data[0]['avatarfull']
        except (KeyError, IndexError): pass
        try:
            realname1 = data[0]['realname']
            realname = realname1.encode('ascii', 'ignore')            
        except (KeyError, IndexError): pass
        try:
            countrycode = data[0]['loccountrycode']
        except (KeyError, IndexError): pass
        
        match_id = p[0] 
        print "MATCH_ID"
        print match_id
        
        
        ############# HER VAR GREIAAAAA #########
#        if player_slot < 128:
#            team_id = p[1] #for radiant team
#            print "TEAM_ID"
#            print team_id
#            cursor.execute("SELECT EXISTS(SELECT id FROM Team WHERE team_id = '%d')" % (team_id))
#            test = cursor.fetchone()[0]
#            if test == 0:
#                cursor.execute("INSERT INTO Team (team_id, team_name) VALUES ('%d', '%s')" % (team_id, 'null'))
#                conn.commit()
#        else:
#            team_id = p[2]
#            print "TEAM_ID"
#            print team_id
#            cursor.execute("SELECT id FROM Team WHERE team_id = '%d'" % (team_id))
#            test = cursor.fetchone()[0]
#            if test == 0:
#                cursor.execute("INSERT INTO Team (team_id, team_name) VALUES ('%d', '%s')" % (team_id, 'null'))
#                conn.commit()

        #for row in datas:
        true = 'true'
        #getMatchDetails
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
        if exists == 1:
            print "player_slot: '%d'" % player_slot
            if player_slot < 128:
                team_id = p[1] #for radiant team
                print "TEAM_ID"
                print team_id
                cursor.execute("SELECT EXISTS(SELECT id FROM Team WHERE team_id = '%d')" % (team_id))
                test = cursor.fetchone()[0]
                if test == 0:
                    cursor.execute("INSERT INTO Team (team_id, team_name) VALUES ('%d', '%s')" % (team_id, 'null'))
                    conn.commit()
            else:
                team_id = p[2]
                print "TEAM_ID"
                print team_id
                cursor.execute("SELECT id FROM Team WHERE team_id = '%d'" % (team_id))
                test = cursor.fetchone()[0]
                if test == 0:
                    cursor.execute("INSERT INTO Team (team_id, team_name) VALUES ('%d', '%s')" % (team_id, 'null'))
                    conn.commit()           
            
            
            
            
            
            end_time = start_time + duration
            cursor.execute("SELECT EXISTS(SELECT id FROM Matches WHERE match_id = '%d')" % (match_id))
            test = cursor.fetchone()[0]
            if test == 0:
                if radiant_win:
                    cursor.execute("INSERT INTO Matches (match_id, tournament_id, winning_team_id, losing_team_id) VALUES ('%d', (SELECT id FROM Tournament WHERE tournament_id = '%d'), '%d', '%d')" % (match_id, league_id, radiant_id, dire_id))
                    conn.commit()
                else:
                    cursor.execute("INSERT INTO Matches (match_id, tournament_id, winning_team_id, losing_team_id) VALUES ('%d', (SELECT id FROM Tournament WHERE tournament_id = '%d'), '%d', '%d')" % (match_id, league_id, dire_id, radiant_id))
                    conn.commit()    


            cursor.execute("SELECT EXISTS(SELECT id FROM Player WHERE player_id = '%d')" % (account_id))
            
            test = cursor.fetchone()[0]
            
            if test == 0:
                print 'INSERT INTO Player'
                
                cursor.execute("INSERT INTO Player (player_id, username, base_rating, display_rating, team_id, avatar, realname, countrycode) VALUES ('%d', '%s', '%d', '%d', (SELECT id from Team WHERE team_id = '%d'), '%s', '%s', '%s')" % (account_id, (username + unichr(300)), 1200, 1200, team_id, avatar, realname, countrycode))
                conn.commit()


            cursor.execute("SELECT EXISTS(SELECT * FROM Player_match WHERE match_id = (SELECT id FROM Matches WHERE match_id = '%d') AND player_id = (SELECT id FROM Player WHERE player_id = '%d'))" % (match_id, account_id))
            test = cursor.fetchone()[0]
            if test == 0:
                print 'INSERT INTO Player_match'
                cursor.execute("INSERT INTO Player_match (match_id, player_id, team_id) VALUES ((SELECT id FROM Matches WHERE match_id = '%d'), (SELECT id FROM Player WHERE player_id = '%d'), '%d')" % (match_id, account_id, team_id))
                conn.commit()

            print "Sleep"
            time.sleep(5)
        









