#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import EloCalc
import probeMethods
import queryParams

dataLeagues = []
dataMatchHistory = []
dataTeamNames = []
dataMatchHistoryPlayers = []
dataTeamPlayers = []
teamID = []
antallKallTot = 0

#probeMethods.setDate(); # Runs ONE TIME before probemodule starts
#Runs one time all the way through
#dataLeagues = [(65001, 'The_International_2012'), (65006, 'The_International'), (600, 'The_International_2014')] #testdata
#dataLeagues = [(19, 'GosuAsiaMadness'),(65007, 'Nexon_Starter_League'), (88, 'LigaBEL') ] #testdata
dataLeagues = probeMethods.getLeagueListing()
for row in dataLeagues:
    league_id = row[0]
    league_name = row[1]
    res = probeMethods.insertTournament(league_id, league_name) #returns 1 if league does not exist, returns 2 if some matches are not registered
    if res == 1:  
        del dataMatchHistory[:]    
        dataMatchHistory = probeMethods.getMatchHistory(league_id) #returns match_id, radiant_team_id, dire_team_id and players
        for row in dataMatchHistory: #for every match
            match_id = row[0] 
            res = probeMethods.checkMatchExist(match_id) #check that match does not already exist, return 1 if true
            if res == 1:
                probeMethods.createTeams(match_id, row[1], row[2]) #adds both teams, if they do not alreay exist
                probeMethods.insertMatches(match_id, league_id, row[1], row[2]) #adda match
                teamID.append(row[1]) 
                teamID.append(row[2])
                for row in teamID: #for both teams
                    team_id = row
                    del dataTeamPlayers[:]
                    dataTeamPlayers = probeMethods.getTeamPlayers(row)
                    for row in dataTeamPlayers:
                        account_id = row
                        steam_id = row + queryParams.steam_number
                        dataPerson = probeMethods.getPlayerSummaries(steam_id) #gets player info
                        for row in dataPerson:
                            if row[0] != None:
                                probeMethods.insertPlayer(account_id, row[0], team_id, row[1], row[2], row[3]) #adds player

                del dataMatchHistoryPlayers[:]
                dataMatchHistoryPlayers = probeMethods.getMatchDetailsPlayers(match_id)
                for row in dataMatchHistoryPlayers:
                    account_id = row[0]
                    check = probeMethods.checkPlayer(account_id)
                    player_slot = row[1]
                    if row[0] != None:
                        if player_slot < 128: #if radiant
                            probeMethods.insertPlayerMatch(match_id, account_id, teamID[0])              
                        else: #if dire
                            probeMethods.insertPlayerMatch(match_id, account_id, teamID[1])
                del teamID[:]   
                EloCalc.calculate2()
    elif res == 2:
        startAtMatchID = probeMethods.getStartAtMatchId(league_id) #deletes the last registered match_id and return the match_id or 0
        del dataMatchHistory[:]    
        if startAtMatchID > 0: #if one or more matches were registered before the interruption
            dataMatchHistory = probeMethods.getMatchHistoryV2(league_id, startAtMatchID)
        else: #if no matches were registered before the interruption
            dataMatchHistory = probeMethods.getMatchHistory(league_id)
        for row in dataMatchHistory:
            match_id = row[0]
            res = probeMethods.checkMatchExist(match_id)
            if res == 1:
                probeMethods.createTeams(match_id, row[1], row[2])
                probeMethods.insertMatches(match_id, league_id, row[1], row[2])
                teamID.append(row[1]) 
                teamID.append(row[2])
                for row in teamID:
                    team_id = row
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
                EloCalc.calculate2()







         
