#!/usr/bin/env python
# -*- coding: utf-8 -*- 

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
from flask.ext.restful import Api
from functools import update_wrapper
import EloCalc

app = Flask(__name__)
api = Api(app)

from flask.ext.cors import CORS
cors = CORS(app) #added

#probeMethods.updatePlayer()
#probeMethods.updateTeam()
#Variables
dataLeagues = []
dataMatchHistory = []
#dataPerson = []
dataTeamNames = []
dataMatchHistoryPlayers = []
dataTeamPlayers = []
teamID = []
antallKallTot = 0


probeMethods.setDate(); # Runs ONE TIME before probemodule starts


#dataLeagues = probeMethods.getLeagueListing()
dataLeagues = [(65001, 'The_International_2012'), (65006, 'The_International'), (600, 'The_International_2014')]
for row in dataLeagues:
    league_id = row[0]
    league_name = row[1]
    res = probeMethods.insertTournament(league_id, league_name) #gir 1 om league ikke eksisterer, gir 2 om ikke alle matcher er registrert
    if res == 1:  
        del dataMatchHistory[:]    
        dataMatchHistory = probeMethods.getMatchHistory(league_id)
        for row in dataMatchHistory:
            match_id = row[0] #Er avhengig av at match_id finnes 
            res = probeMethods.checkMatchExist(match_id)
            if res == 1:
                print "MATCH_ID: ", match_id
                probeMethods.createTeams(match_id, row[1], row[2])
                probeMethods.insertMatches(match_id, league_id, row[1], row[2])
                teamID.append(row[1]) 
                teamID.append(row[2])
                for row in teamID:
                    team_id = row
                    print "TEAM_ID: ", row
                    del dataTeamPlayers[:]
                    dataTeamPlayers = probeMethods.getTeamPlayers(row)
                    for row in dataTeamPlayers:
                        account_id = row
                        steam_id = row + queryParams.steam_number
                        dataPerson = probeMethods.getPlayerSummaries(steam_id)
                        for row in dataPerson:
                            if row[0] != None:
                                probeMethods.insertPlayer(account_id, row[0], team_id, row[1], row[2], row[3]) 

                del dataMatchHistoryPlayers[:]
                dataMatchHistoryPlayers = probeMethods.getMatchDetailsPlayers(match_id)
                for row in dataMatchHistoryPlayers:
                    account_id = row[0]
                    check = probeMethods.checkPlayer(account_id)
                    player_slot = row[1]
                    if row[0] != None:
                        if player_slot < 128:
                            probeMethods.insertPlayerMatch(match_id, account_id, teamID[0])              
                        else:
                            probeMethods.insertPlayerMatch(match_id, account_id, teamID[1])
                del teamID[:] 
                probeMethods.calculate(match_id)
            antallKall = probeMethods.APIcalls()
            antallKallTot += antallKall
            print "antallKall: ", antallKall
            print "antallKallTot: ", antallKallTot        
    elif res == 2:
        startAtMatchID = probeMethods.getStartAtMatchId(league_id)
        print "Kjører versjon 2 fra match_id: ", startAtMatchID
        del dataMatchHistory[:]    
        if startAtMatchID > 0:
            dataMatchHistory = probeMethods.getMatchHistoryV2(league_id, startAtMatchID)
        else:
            dataMatchHistory = probeMethods.getMatchHistory(league_id)
        for row in dataMatchHistory:
            match_id = row[0] #Er avhengig av at match_id finnes 
            res = probeMethods.checkMatchExist(match_id)
            print "RES: ", res
            if res == 1:
                print "MATCH_ID: ", match_id
                probeMethods.createTeams(match_id, row[1], row[2])
                probeMethods.insertMatches(match_id, league_id, row[1], row[2])
                teamID.append(row[1]) 
                teamID.append(row[2])
                for row in teamID:
                    team_id = row
                    print "TEAM_ID: ", row
                    del dataTeamPlayers[:]
                    dataTeamPlayers = probeMethods.getTeamPlayers(row)
                    for row in dataTeamPlayers:
                        account_id = row
                        steam_id = row + queryParams.steam_number
                        dataPerson = probeMethods.getPlayerSummaries(steam_id)
                        for row in dataPerson:
                            if row[0] != None:
                                probeMethods.insertPlayer(account_id, row[0], team_id, row[1], row[2], row[3]) 

                del dataMatchHistoryPlayers[:]
                dataMatchHistoryPlayers = probeMethods.getMatchDetailsPlayers(match_id)
                for row in dataMatchHistoryPlayers:
                    account_id = row[0]
                    check = probeMethods.checkPlayer(account_id)
                    player_slot = row[1]
                    if row[0] != None:
                        if player_slot < 128:
                            probeMethods.insertPlayerMatch(match_id, account_id, teamID[0])              
                        else:
                            probeMethods.insertPlayerMatch(match_id, account_id, teamID[1])
                del teamID[:] 
                EloCalc.calculate(match_id)
            antallKall = probeMethods.APIcalls()
            antallKallTot += antallKall
            print "antallKall: ", antallKall
            print "antallKallTot: ", antallKallTot
                            
##            print dire_team_id
##            probeMethods.insertMatches(match_id, league_id, radiant_team_id, dire_team_id)
##            del dataMatchHistoryPlayers[:]
##            dataMatchHistoryPlayers = probeMethods.getMatchDetailsPlayers(match_id)
##            for rowrow in dataMatchHistoryPlayers:
##                account_id = rowrow[0]
##                player_slot = rowrow[1]
##                steam_id = account_id + queryParams.steam_number ####*****OBSOBS, SJEKK OM DETTA FUNKER
##                dataTeamNames = probeMethods.getMatchDetailsTeamName(match_id)
##                probeMethods.insertTeam(radiant_team_id, dataTeamNames[0][0])
##                probeMethods.insertTeam(dire_team_id, dataTeamNames[0][1])
##                del dataTeamNames[:]
##                dataPerson = probeMethods.getPlayerSummaries(steam_id)
##                for row in dataPerson:
##                    if row[0] != None:
##                        if player_slot < 128:
##                            del dataTeamPlayers[:]
##                            dataTeamPlayers = probeMethods.getTeamPlayers
##                            for row in dataTeamPlayers:
##                                cursor.execute
##                            #probeMethods.insertPlayer(account_id, row[0], radiant_team_id, row[1], row[2], row[3]) 
##                            probeMethods.insertPlayerMatch(match_id, account_id, radiant_team_id)
##                        else:
##                            #probeMethods.insertPlayer(account_id, row[0], dire_team_id, row[1], row[2], row[3])
##                            probeMethods.insertPlayerMatch(match_id, account_id, dire_team_id)
#                            
#                            
#                            
#                            
##            for rowrow in dataMatchHistoryPlayers:
##                account_id = rowrow[0]
##                player_slot = rowrow[1]
##                steam_id = account_id + queryParams.steam_number ####*****OBSOBS, SJEKK OM DETTA FUNKER
##                dataTeamNames = probeMethods.getMatchDetailsTeamName(match_id)
##                probeMethods.insertTeam(radiant_team_id, dataTeamNames[0][0])
##                probeMethods.insertTeam(dire_team_id, dataTeamNames[0][1])
##                del dataTeamNames[:]
##                dataPerson = probeMethods.getPlayerSummaries(steam_id)
##                for row in dataPerson:
##                    if row[0] != None:
##                        if player_slot < 128:
##                            probeMethods.insertPlayer(account_id, row[0], radiant_team_id, row[1], row[2], row[3]) 
##                            probeMethods.insertPlayerMatch(match_id, account_id, radiant_team_id)
##                        else:
##                            probeMethods.insertPlayer(account_id, row[0], dire_team_id, row[1], row[2], row[3])
##                            probeMethods.insertPlayerMatch(match_id, account_id, dire_team_id)
#                
