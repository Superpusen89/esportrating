from flask import Flask, request
import MySQLdb
import requests
import pprint
import urllib
import json
import queryParams
import time
import probeMethods
import queries

#try:
#    conn = MySQLdb.connect(host="localhost", user="root", passwd="HenrietteIda", db="esportrating", charset='utf8', use_unicode=True)
#    cursor = conn.cursor()
#    
#except MySQLdb.Error, e:
#    print "Error %d: %s" % (e.args[0], e.args[1])
#    sys.exit(1)

probeMethods.openDatabaseConn()
    
#Variables
dataLeagues = []
dataMatchHistory = []
#dataPerson = []
dataTeamNames = []
dataMatchHistoryPlayers = []


dataLeagues = probeMethods.getLeagueListing()
print len(dataLeagues)
for row in dataLeagues:
    league_id = row[0]
    league_name = row[1]
    res = probeMethods.insertTournament(league_id, league_name)
    if res == 1:     
        del dataMatchHistory[:]    
        dataMatchHistory = probeMethods.getMatchHistory(league_id)
        
        pprint.pprint(dataMatchHistory[0])
        for row in dataMatchHistory:
            match_id = row[0]
            print "match_id: ", match_id
            radiant_team_id = row[1]
            print radiant_team_id
            dire_team_id = row[2]
            print dire_team_id
            probeMethods.insertMatches(match_id, league_id, radiant_team_id, dire_team_id)
            del dataMatchHistoryPlayers[:]
            dataMatchHistoryPlayers = probeMethods.getMatchDetailsPlayers(match_id)
            for rowrow in dataMatchHistoryPlayers:
                account_id = rowrow[0]
                player_slot = rowrow[1]
                steam_id = account_id + 76561197960265728
                dataTeamNames = probeMethods.getMatchDetailsTeamName(match_id)
                probeMethods.insertTeam(radiant_team_id, dataTeamNames[0][0])
                probeMethods.insertTeam(dire_team_id, dataTeamNames[0][1])
                del dataTeamNames[:]
                dataPerson = probeMethods.getPlayerSummaries(steam_id)
                for row in dataPerson:
                    if row[0] != None:
                        if player_slot < 128:
                            probeMethods.insertPlayer(account_id, row[0], radiant_team_id, row[1], row[2], row[3]) 
                            probeMethods.insertPlayerMatch(match_id, account_id, radiant_team_id)
                        else:
                            probeMethods.insertPlayer(account_id, row[0], dire_team_id, row[1], row[2], row[3])
                            probeMethods.insertPlayerMatch(match_id, account_id, dire_team_id)
                
