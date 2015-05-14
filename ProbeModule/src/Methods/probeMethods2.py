#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import MySQLdb
from decimal import Decimal
from flask import Flask
from flask import json
from flask import jsonify
from flask import request
from functools import update_wrapper
import json
import math
import pprint
import queries
import queryParams
import requests
import sys
import urllib

try:
    conn = MySQLdb.connect(host="localhost", user="root", passwd="HenrietteIda", db="esportrating", use_unicode=True, charset='utf8', )
    conn.autocommit(True)
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
dataTeamPlayers = []
dataPlayers = []
numAPI = 0



def openDatabaseConn():
    try:
        conn = MySQLdb.connect(host="localhost", user="root", passwd="HenrietteIda", db="esportrating", use_unicode=True, charset='utf8')
        cursor = conn.cursor()

    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)   


def getLeagueListing():
    response = requests.get(queryParams.endpoint1, params=queryParams.query_params1)
    numAPI = 2
    try:
        data = response.json()['result']['leagues']
    except KeyError: pass
    for row in data:
        dataLeague.append([row['leagueid'], row['name']])
    return dataLeague

def getMatchHistory(league_id):
    del dataMatchHistory[:]
    query_params2 = {'key': queryParams.key,
        'league_id': league_id 
            }
    response = requests.get(queryParams.endpoint2, params=query_params2)
    try:    
        data = response.json()['result']['matches']
    except KeyError: pass
    for row in data:
        dataMatchHistory.append([row['match_id'], row['radiant_team_id'], row['dire_team_id'], row['players']])
    return dataMatchHistory

def getMatchDetailsPlayers(match_id):
    print "getMatcgDetailsPlayers"
    del dataMatchHistoryPlayers[:]
    query_params3 = {'key': queryParams.key,
        'match_id': match_id 
            }
    response = requests.get(queryParams.endpoint3, params=query_params3)
    try:
        data = response.json()['result']['players']
    except KeyError: pass
    for row in data:
        dataMatchHistoryPlayers.append([row['account_id'], row['player_slot']])
    return dataMatchHistoryPlayers

def getTeamPlayers(team_id):
    del dataTeamPlayers[:]
    query_params5 = {'key': queryParams.key,
        'start_at_team_id': team_id,
        'teams_requested': 1
            }
    try:
        response = requests.get(queryParams.endpoint5, params=query_params5)
        data = response.json()['result']['teams']
    except KeyError: pass
    try:
        player0 = data[0]['player_0_account_id']
        dataTeamPlayers.append(player0)
        player1 = data[0]['player_1_account_id']
        dataTeamPlayers.append(player1)
        player2 = data[0]['player_2_account_id']
        dataTeamPlayers.append(player2)
        player3 = data[0]['player_3_account_id']
        dataTeamPlayers.append(player3)
        player4 = data[0]['player_4_account_id']
        dataTeamPlayers.append(player4)
        player5 = data[0]['player_5_account_id']
        dataTeamPlayers.append(player5)
        player6 = data[0]['player_6_account_id']
        dataTeamPlayers.append(player6)
    except KeyError: pass
    return dataTeamPlayers
    

def getPlayerSummaries(steam_id):
    del dataPerson[:]
    query_params4 = {'key': queryParams.key,
        'steamids': steam_id
            } 
    try:
        response = requests.get(queryParams.endpoint4, params=query_params4)
        data = response.json()['response']['players']
    except KeyError: pass
    for row in data:
        username = 'null' # IKKE ALLE SOM HAR AAPEN PROFIL
        avatar = 'null'
        realname = 'null'
        countrycode = 'null'
        try:
            personaname = data[0]['personaname']
            username = personaname.encode('utf-8')
            try:
                avatar = data[0]['avatarfull']
            except (KeyError, IndexError): pass
            try:
                realname1 = data[0]['realname']
                realname = realname1.encode('utf-8')     
            except (KeyError, IndexError): pass
            try:
                countrycode = data[0]['loccountrycode']
            except (KeyError, IndexError): pass
        except (KeyError, IndexError): pass
        
        dataPerson.append([username, avatar, realname, countrycode])
        
    return dataPerson

def getPlayerUsername(steam_id):
    query_params4 = {'key': queryParams.key,
        'steamids': steam_id
            } 
    try:
        response = requests.get(queryParams.endpoint4, params=query_params4)
        data = response.json()['response']['players']
    except KeyError: pass
    for row in data:
        username = 'null'
        try:
            personaname = data[0]['personaname']
            username = personaname #.encode('ascii', 'ignore')
        except (KeyError, IndexError): pass
    return username


def getPlayerSummariesver2(steam_id):
    del dataPerson[:]
    query_params4 = {'key': queryParams.key,
        'steamids': steam_id
            } 
    try:
        response = requests.get(queryParams.endpoint4, params=query_params4)
        data = response.json()['response']['players']
    except KeyError: pass
    for row in data:
        username = 'null' # IKKE ALLE SOM HAR AAPEN PROFIL
        avatar = 'null'
        realname = 'null'
        countrycode = 'null'
        try:
            personaname = data[0]['personaname']
            username = personaname # .encode('utf-8', 'ignore')
            print username
            try:
                avatar = data[0]['avatarfull']
            except (KeyError, IndexError): pass
            try:
                realname1 = data[0]['realname']
                realname = realname1 #.encode('ascii', 'ignore')     
            except (KeyError, IndexError): pass
            try:
                countrycode = data[0]['loccountrycode']
            except (KeyError, IndexError): pass
        except (KeyError, IndexError): pass
        
        dataPerson.append([username, avatar, realname, countrycode])
    return dataPerson

def getPlayerUsername(steam_id):
    query_params4 = {'key': queryParams.key,
        'steamids': steam_id
            } 
    try:
        response = requests.get(queryParams.endpoint4, params=query_params4)
        data = response.json()['response']['players']
    except KeyError: pass
    for row in data:
        username = 'null'
        try:
            personaname = data[0]['personaname']
            username = personaname #.encode('ascii', 'ignore')
        except (KeyError, IndexError): pass
    return username
    
            
    
def getMatchDetailsTeamName(match_id):
    #del dataTeamNames[:]
    query_params3 = {'key': queryParams.key,
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

def insertTournament(league_id, league_name):
    cursor.execute(queries.q1, [league_id])
    test = cursor.fetchone()[0]
    dataMatchHistory = getMatchHistory(league_id)
    lenMatches = len(dataMatchHistory) #checks that every match has been registered, if not; run through again
    cursor.execute(queries.q18, [league_id])
    actualLenMatches = cursor.fetchone()[0]
    if test == 0:
        cursor.execute(queries.q2, ([league_id, league_name]))
        conn.commit()
        return 1
    if actualLenMatches < lenMatches:
        return 1
    return -1

def insertTeam(team_id, team_name):
    cursor.execute(queries.q3, [team_id])
    test = cursor.fetchone()[0]
    if test == 0 and team_name != None:
        cursor.execute(queries.q4, [team_id, team_name])
        conn.commit()

def insertPlayer(account_id, username, team_id, avatar, realname, countrycode):
    cursor.execute(queries.q5, [account_id])
    test = cursor.fetchone()[0]
    if test == 0:
        cursor.execute(queries.q6, [account_id, username, 1200, 1200, team_id, avatar, realname, countrycode]) #(username + unichr(300))
        conn.commit()
        
def insertPlayerVer1(account_id, team_id):
    cursor.execute(queries.q5, [account_id])
    test = cursor.fetchone()[0]
    if test == 0:
        steam_id = account_id + queryParams.steam_number
        dataPlayers = getPlayerSummaries(steam_id)
        for row in dataPlayers:
            if row[0] != None:
                cursor.execute(queries.q6, [account_id, row[0], 1200, 1200, row[1], row[2], row[3]]) #(username + unichr(300))
                conn.commit()
        del dataPlayers[:]
        
def insertPlayerVer2(account_id):
    cursor.execute(queries.q5 % (account_id))
    test = cursor.fetchone()[0]
    if test == 0:
        steam_id = account_id + queryParams.steam_number
        dataPlayers = getPlayerSummaries(steam_id)
        for row in dataPlayers:
            if row[0] != None:
                cursor.execute(queries.q17, [account_id, row[0], 1200, 1200, row[1], row[2], row[3]]) #(username + unichr(300))
                conn.commit()
        del dataPlayers[:]
        
def insertMatches(match_id, league_id, radiant_team_id, dire_team_id):
    radiant_win = None
    query_params3 = {'key': queryParams.key,
        'match_id': match_id 
            }
    response = requests.get(queryParams.endpoint3, params=query_params3)
    try:
        start_time = response.json()['result']['start_time']
        duration = response.json()['result']['duration']
        radiant_win = response.json()['result']['radiant_win']
    except KeyError: pass
    if radiant_win != None: #AND timestamp?
        end_time = start_time + duration
        cursor.execute(queries.q7, [match_id])
        test = cursor.fetchone()[0]
        if test == 0:
            if radiant_win:
                cursor.execute(queries.q8, [match_id, league_id, radiant_team_id, dire_team_id, radiant_team_id, dire_team_id, start_time, end_time])
                conn.commit()
            else:
                cursor.execute(queries.q9, [match_id, league_id, radiant_team_id, dire_team_id, dire_team_id, radiant_team_id, start_time, end_time])
                conn.commit() 
    

def insertPlayerMatch(match_id, account_id, team_id):
    cursor.execute(queries.q10, [match_id, account_id])
    test = cursor.fetchone()[0]
    if test == 0:
        cursor.execute(queries.q11, [match_id, account_id, team_id])
        conn.commit()
        
        
def createTeams(match_id, team_1, team_2):
    dataTeamNames = getMatchDetailsTeamName(match_id)
    insertTeam(team_1, dataTeamNames[0][0])
    insertTeam(team_2, dataTeamNames[0][1])
    del dataTeamNames[:]

def updatePlayer():
    cursor.execute(queries.q12)
    data = cursor.fetchall();
    for row in data:
        steam_id = row[1] + queryParams.steam_number
        username = getPlayerUsername(steam_id)
        if row[0] != username:
            cursor.execute(queries.q13, [username, row[1]])
            conn.commit()
            
def updatePlayer2():
    cursor.execute(queries.q16)
    data = cursor.fetchall();
    cursor.execute(queries.q)
    for row in data:
        steam_id = row[1] + queryParams.steam_number
        username = getPlayerUsername(steam_id)
        team_id = row[2]
        if row[0] != username:
            cursor.execute(queries.q13, [username, row[1]])
            conn.commit()
        
def updateTeam():
    cursor.execute(queries.q14)
    data = cursor.fetchall()
    for row in data:
        team_id = row[0]
        query_params5 = {'key': queryParams.key,
            'start_at_team_id': team_id,
            'teams_requested': 1
                }
        try:
            response = requests.get(queryParams.endpoint5, params=query_params5)
            data = response.json()['result']['teams']
        except KeyError: pass
        team_name = data[0]['name']
        if row[1] != team_name:
            cursor.execute(queries.q15, [team_name, row[0]])
            conn.commit()
        
def checkPlayer(account_id):
    cursor.execute(queries.q16, [account_id])
    test = cursor.fetchone()[0]
    if test == 0:
        insertPlayerVer2(account_id)
    return "PLAYER INSERTED"

def checkMatchExist(match_id):
    cursor.execute(queries.q7, [match_id])
    test = cursor.fetchone()[0]
    if test == 0:
        return 1;
    else:
        print "Hopper over match ", match_id
        return -1;
   
            
def check(match_id):
    cursor.execute("SELECT COUNT(points) FROM Player_match WHERE match_id = (SELECT id FROM Matches WHERE match_id = %s", [match_id])
    count = cursor.fetchone()[0]
    if(count != 0):
        resetDisplayRating(match_id)

def resetDisplayRating(match_id):
    cursor.execute("SELECT points, player_id FROM Player_match WHERE match_id=(SELECT id FROM Matches WHERE match_id = %s", [match_id]) #MATCH_ID
    pointsExist = cursor.fetchall()
    for row in pointsExist:
        player_id = Decimal(row[1])
        points = Decimal(row[0])
        if(points != null):
            cursor.execute("SELECT display_rating FROM Player WHERE id = %s", [player_id])
            display_rating = Decimal(cursor.fetchone()[0])
            newDisplay_rating = display_rating - points
            print Display_rating
            cursor.execute("UPDATE Player SET display_rating = %s WHERE id = %s", [newDisplay_rating, player_id])
            conn.commit()
        
def setDisplayRating(match_id):
    cursor.execute("SELECT pm.points, p.id FROM Player_match pm, Player p WHERE match_id=(SELECT id FROM Matches WHERE match_id = %s) AND pm.player_id=p.id", [match_id])
    data = cursor.fetchall()
    for row in data:
        points = float(row[0])
        player_id = float(row[1])
        cursor.execute("SELECT display_rating FROM Player WHERE id = %s", [player_id])
        display_rating = float(cursor.fetchone()[0])
        newDisplay_rating = display_rating + points
        cursor.execute("UPDATE Player SET display_rating = %s WHERE id = %s", [newDisplay_rating, player_id])
        conn.commit()
        
def calculate(match_id):
    team1 = 'winning_team_id'
    team2 = 'losing_team_id'
    print "match_id i kalkis: ", match_id
    cursor.execute(queries.findAVG3, [match_id, match_id]) #finds losing team's average score
    B = float(cursor.fetchone()[0])
    cursor.execute(queries.findAVG4, [match_id, match_id]) #finds winning team's average score
    A = float(cursor.fetchone()[0])
    
    #Elo-rating formula
    Es = 1.0 / (1.0 + math.pow(10.0, ((B-A) / 400.0)))
    print "Es: ", Es 
    R = round(Decimal(15 * (1-Es)), 2) #winning team points
    print "R: ", R
    cursor.execute(queries.findID1, [match_id, match_id]) #finds every participating player on winning team
    ID = cursor.fetchall()
    for row in ID: #for each player -> update points
        id = row[0]
        print "for each player -> update points", id
        cursor.execute(queries.updatePoints, [R, match_id, id])
        conn.commit()
    R = -R #losing team points
    cursor.execute(queries.findID2, [match_id, match_id]) #finds every participating player on winning team
    ID = cursor.fetchall()
    for row in ID: #for each player -> update points
        id = row[0]
        print "for each player -> update points", id
        cursor.execute(queries.updatePoints, [R, match_id, id])
        conn.commit()
    setDisplayRating(match_id) #run this method
    

        
def APIcalls():
    res = numberAPI
    numberAPI = 0
    return res
 
        
        