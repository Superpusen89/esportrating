import queryParams
from flask import Flask, request
from configparser import ConfigParser
from python_mysql_dbconfig import read_db_config
from mysql.connector import MySQLConnection, Error
import MySQLdb
import requests
import pprint
import urllib
import json
import queries
import sys



#Variables
dataLeague = []
dataMatchHistory = []
dataPerson = []
dataTeamNames = []
dataMatchHistoryPlayers = []


def openDatabaseConn():
    db_config = read_db_config()
    
    try:
        print('Connecting to MySQL database...')
        conn = MySQLConnection(**db_config)
        cursor = conn.cursor()
#        if conn.is_connected():
#            
#            print('connection established.')
#        else:
#            print('connection failed.')
 
    except Error as error:
        print(error)
 
#    finally:
#        conn.close()
#        print('Connection closed.')
    
#    try:
#        conn = MySQLdb.connect(**db_config)
#        cursor = conn.cursor()
#        print "database OK"
#
#    except MySQLdb.Error, e:
#        print "Error %d: %s" % (e.args[0], e.args[1])
#        sys.exit(1)


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

def insertTournament(league_id, league_name):
    cursor.execute(queries.q1 % (league_id))
    test = cursor.fetchone()[0]
    if test == 0:
        cursor.execute(queries.q2 % (league_id, league_name))
        conn.commit()
        return 1
    return -1

def insertTeam(team_id, team_name):
    cursor.execute(queries.q3 % (team_id))
    test = cursor.fetchone()[0]
    if test == 0:
        cursor.execute(queries.q4 % (team_id, team_name))
        conn.commit()

def insertPlayer(account_id, username, team_id, avatar, realname, countrycode):
    cursor.execute(queries.q5 % (account_id))
    test = cursor.fetchone()[0]
    if test == 0:
        cursor.execute(queries.q6 % (account_id, (username + unichr(300)), 1200, 1200, team_id, avatar, realname, countrycode))
        conn.commit()
        
def insertMatches(match_id, league_id, radiant_team_id, dire_team_id):
    radiant_win = None
    query_params3 = { 'key': queryParams.key,
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
        cursor.execute(queries.q7 % (match_id))
        test = cursor.fetchone()[0]
        if test == 0:
            if radiant_win:
                cursor.execute(queries.q8 % (match_id, league_id, radiant_team_id, dire_team_id, start_time, end_time))
                conn.commit()
            else:
                cursor.execute(queries.q9 % (match_id, league_id, dire_team_id, radiant_team_id, start_time, end_time))
                conn.commit() 
    

def insertPlayerMatch(match_id, account_id, team_id):
    cursor.execute(queries.q10 % (match_id, account_id))
    test = cursor.fetchone()[0]
    if test == 0:
        print 'INSERT INTO Player_match'
        cursor.execute(queries.q11 % (match_id, account_id, team_id))
        conn.commit()