#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import MySQLdb
from datetime import timedelta

from decimal import Decimal
from flask import Flask
from flask import current_app
from flask import json
from flask import jsonify
from flask import make_response
from flask import request
from flask.ext.restful import Api
from flask.ext.restful import Resource
from flask.ext.restful import fields
from flask.ext.restful import marshal
from flask.ext.restful import reqparse
from functools import update_wrapper
import math
import queries
import sys
import time
import datetime
import databaseconnector

app = Flask(__name__)
api = Api(app)

from flask.ext.cors import CORS
cors = CORS(app) #added

try:
    conn = MySQLdb.connect(host="localhost", user="root", passwd="HenrietteIda", db="esportrating", use_unicode=True, charset="utf8")
    conn.autocommit(True)
    cursor = conn.cursor()
#    cursor.execute("SET NAMES utf8;")
#    cursor.execute("SET NAMES utf8mb4;") #or utf8 or any other charset you want to handle
#    cursor.execute("SET CHARACTER SET utf8mb4;") #same as above
#    cursor.execute("SET character_set_connection=utf8mb4;") #same as above
    
except MySQLdb.Error, e:
    print "Error %d: %s" % (e.args[0], e.args[1])
    sys.exit(1)

#cursor = databaseconnector.databaseConn();


def getMonth():
    month = datetime.datetime.now().month
    print "month: ", month
    cursor.execute(queries.q24)
    prevMonth = cursor.fetchone()[0]
    print "prevMonth: ", prevMonth
    if month != prevMonth:
        cursor.execute(queries.q26 % [month])
        conn.commit()
        updateBaseRating()
    return 0


def setDisplayRating(match_id):
    cursor.execute("SELECT pm.points, p.id FROM Player_match pm, Player p WHERE match_id='%s' AND pm.player_id=p.id" % (match_id))
    data = cursor.fetchall()
    for row in data:
        points = float(row[0])
        player_id = float(row[1])
        cursor.execute("SELECT display_rating FROM Player WHERE id = '%s'" % player_id)
        display_rating = float(cursor.fetchone()[0])
        newDisplay_rating = display_rating + points
        cursor.execute("UPDATE Player SET display_rating = '%s' WHERE id = '%d'" % (newDisplay_rating, player_id))
        conn.commit()
       
def check(match_id):
    cursor.execute("SELECT COUNT(points) FROM Player_match WHERE match_id = '%s'" % (match_id))
    count = cursor.fetchone()[0]
    if(count != 0):
        resetDisplayRating(match_id)

def resetDisplayRating(match_id):
    cursor.execute("SELECT points, player_id FROM Player_match WHERE match_id='%s'" % (match_id)) #MATCH_ID
    pointsExist = cursor.fetchall()
    for row in pointsExist:
        player_id = Decimal(row[1])
        points = Decimal(row[0])
        if(points != None):
            cursor.execute("SELECT display_rating FROM Player WHERE id = '%s'" % (player_id))
            display_rating = Decimal(cursor.fetchone()[0])
            newDisplay_rating = display_rating - points
            print display_rating
            print newDisplay_rating
            cursor.execute("UPDATE Player SET display_rating = '%s' WHERE id = '%d'" % (newDisplay_rating, player_id))
            conn.commit()
    

def eloCalc(match_id):
    getMonth()
    print "match_id i kalkis: ", match_id
    cursor.execute(queries.findAVG1, [match_id, match_id]) #finds losing team's average score
    B = float(cursor.fetchone()[0])
    print "B: ", B
    cursor.execute(queries.findAVG2, [match_id, match_id]) #finds winning team's average score
    A = float(cursor.fetchone()[0])
    print "A: ", A
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
#    
#    team1 = 'winning_team_id'
#    team2 = 'losing_team_id'
#    cursor.execute(queries.findAVG2 % (match_id, team2, match_id)) #finds losing team's average score
#    B = float(cursor.fetchone()[0])
#    print "B probe: ", B
#    cursor.execute(queries.findAVG2 % (match_id, team1, match_id)) #finds winning team's average score
#    A = float(cursor.fetchone()[0])
#    print "A probe: ", A
#    
#    #Elo-rating formula
#    Es = 1.0 / (1.0 + math.pow(10.0, ((B-A) / 400.0)))
#    print "Es: '%s'" % Es 
#    R = round(Decimal(15 * (1-Es)), 2) #winning team points
#    
#    cursor.execute(queries.findID % (match_id, team1, match_id)) #finds every participating player on winning team
#    ID = cursor.fetchall()
#    for row in ID: #for each player -> update points
#        id = row[0]
#        cursor.execute(queries.updatePoints % (R, match_id, id))
#        conn.commit()
#    R = -R #losing team points
#    cursor.execute(queries.findID % (match_id, team2, match_id)) #finds every participating player on winning team
#    ID = cursor.fetchall()
#    for row in ID: #for each player -> update points
#        id = row[0]
#        cursor.execute(queries.updatePoints % (R, match_id, id))
#        conn.commit()
#    setDisplayRating(match_id) #run this method
       



#acces-control-allow-origin
def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, ** kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, ** kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers


            h['Access-Control-Allow-Headers'] = "Origin, X-Requested-With, Content-Type, Accept, Options" 
            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            #h['Access-Control-Allow-Methods'] = 'GET','PUT','POST','DELETE','OPTIONS'
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator   


#def Elo_calc(match_id):
#    cursor.execute("SELECT AVG(base_rating) FROM Player WHERE id= ANY (SELECT player_id FROM Player_match WHERE match_id = 1) AND team_id=(SELECT winning_team_id FROM Matches WHERE id=1)")
#    B = cursor.fetchone()
#    cursor.execute("SELECT base_rating FROM Player WHERE id= ANY (SELECT player_id FROM Player_match WHERE match_id = 1) AND team_id=(SELECT losing_team_id FROM Matches WHERE id=1)") #Maa finne baseratinga til alle spillerne som har vaert med paa denne kampen
#    A = cursor.fetchone()
#    while A is not None:
#        #Es = 1/(1+10^((B-A)/400))
#        print A;
    #SELECT base_rating FROM Player WHERE id= ANY (SELECT player_id FROM Player_match WHERE match_id = 1) AND team_id=(SELECT losing_team_id FROM Matches WHERE id=1);
    #isSet = ("SELECT points FROM")
    
#remove this? 
#@app.route('/player/<username>', methods=['GET', 'OPTIONS'])
#@crossdomain(origin='*')
#def get_player_name(username):
#        print ("Hallohallo")
#        #username = request.get_json().get('username', '')
#        print ("Hallohalloigjen")
#        print request.args.get('username')
#        cursor.execute("SELECT username, display_rating FROM Player WHERE username = '%s'" % (username))
#        data = [dict(line) for line in [zip([column[0] for column in cursor.description], 
#                                            row) for row in cursor.fetchall()]]
#        
#        return jsonify(data=data)

@app.route('/player/<int:player_id>', methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
def get_player(player_id):
    cursor.execute("SELECT avatar, p.id, countrycode, username, display_rating, base_rating, team_name, p.team_id FROM (Player p join Team t on p.team_id = t.id) WHERE p.id = '%d'" % (player_id))
    data = [dict(line) for line in [zip([column[0] for column in cursor.description], 
                                        row) for row in cursor.fetchall()]]
    return jsonify(data=data)

@app.route('/team_player/<int:team_id>', methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
def get_team_player(team_id):
    cursor.execute("SELECT * FROM Player WHERE team_id = '%d'" % (team_id))
    data = [dict(line) for line in [zip([column[0] for column in cursor.description], 
                                        row) for row in cursor.fetchall()]]
    return jsonify(data=data)

@app.route('/player', methods=['POST', 'OPTIONS'])
@crossdomain(origin='*')
def create_player():
    username = request.get_json().get('username', '')
    team_id = request.get_json().get('team_id', '')
    avatar = request.get_json().get('avatar', '')
    real_name = request.get_json().get('real_name', '')
    country = request.get_json().get('country', '')
        
    if len(country) != 2:
        country = 'null';
        
    if len(str(team_id)) == 0:
        cursor.execute("INSERT INTO Player (username, base_rating, display_rating, avatar, realname, countrycode) VALUES (%s, %s, %s, %s, %s, %s)" , [username, 1200, 1200, avatar, real_name, country]) 
    elif len(str(team_id)) != 0:    
        cursor.execute("INSERT INTO Player (username, base_rating, display_rating, team_id, avatar, realname, countrycode) VALUES (%s, %s, %s, %s, %s, %s, %s)" , [username, 1200, 1200, team_id, avatar, real_name, country])
    
    conn.commit()
    return "%s is added" % username
        

@app.route('/player', methods=['PUT', 'OPTIONS'])
@crossdomain(origin='*')
def edit_player():
    player_id = request.get_json().get('player_id', '')
    username = request.get_json().get('username', '')
    team_id = request.get_json().get('team_id', '')
    base_rating = request.get_json().get('base_rating', '')
    dispaly_rating = request.get_json().get('display_rating', '')
    cursor.execute("UPDATE Player SET username = '%s', base_rating = '%d', display_rating = '%d', team_id = '%d' where id = '%d'" % (username, base_rating, dispaly_rating, team_id, player_id))
    conn.commit()
    return "%s is updated!" % username

@app.route('/team/<int:team_id>', methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
def get_team(team_id):
    cursor.execute("SELECT * FROM Team WHERE id = '%d'" % (team_id))
    data = [dict(line) for line in [zip([column[0] for column in cursor.description], 
                                        row) for row in cursor.fetchall()]]
        
    return jsonify(data=data)
    
@app.route('/team/<team_name>', methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
def get_team_by_name(team_name):
    cursor.execute("SELECT id FROM Team WHERE team_name = '%s'" % (team_name))
    data = [dict(line) for line in [zip([column[0] for column in cursor.description], 
                                        row) for row in cursor.fetchall()]]
        
    return jsonify(data=data)

@app.route('/team', methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
def get_teams():
    cursor.execute("SELECT * FROM Team")
#    cat = '哈哈'
    data = [dict(line) for line in [zip([column[0] for column in cursor.description], 
                                        row) for row in cursor.fetchall()]]
        
    return jsonify(data=data)

@app.route('/team', methods=['POST', 'OPTIONS'])
@crossdomain(origin='*')
def create_teams():
    #team_id = request.get_json().get('team_id', '')
    team_name = request.get_json().get('team_name', '')
#    q = queries.insertTeam
#    cursor.execute("INSERT INTO Team (team_name) VALUES ('%s')" % (team_name))
    cursor.execute('INSERT INTO Team (team_name) VALUES (%s)', [team_name])
#    cursor.execute('INSERT INTO Team (team_name) VALUES (kåre)')
    conn.commit()
    #return "%s is added" % team_name

    cursor.execute("SELECT LAST_INSERT_ID()")
    team_id = cursor.fetchone()[0]
    return "%d" % team_id; 
        
#    cursor.execute("select * from Matches")
#    data = [dict(line) for line in [zip([column[0] for column in cursor.description], 
#                                        row) for row in cursor.fetchall()]]

    return jsonify(data=team_id)

@app.route('/team', methods=['PUT', 'OPTIONS'])
@crossdomain(origin='*')
def edit_team():
    team_id = request.get_json().get('team_id', '')
    team_name = request.get_json().get('team_name', '')
    cursor.execute("UPDATE Team SET team_name = '%s' where id = '%d'" % (team_name, team_id))
    conn.commit()
    return "%s is updated!" % team_id

@app.route('/tournament/<int:tournament_id>', methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
def get_tournament(tournament_id):
    cursor.execute("SELECT * FROM Tournament WHERE id = '%d'" % (tournament_id))
    data = [dict(line) for line in [zip([column[0] for column in cursor.description], 
                                        row) for row in cursor.fetchall()]]
    return jsonify(data=data)

@app.route('/tournament', methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
def get_tournaments():
    cursor.execute("select * from Tournament")
    data = [dict(line) for line in [zip([column[0] for column in cursor.description], 
                                        row) for row in cursor.fetchall()]]
    return jsonify(data=data)

@app.route('/tournament', methods=['POST', 'OPTIONS'])
@crossdomain(origin='*')
def create_tournament():
    # tournament_id = request.get_json().get('tournament_id', '')
        tournament_name = request.get_json().get('tournament_name', '')
        cursor.execute("INSERT INTO Tournament (tournament_name) VALUES ('%s')" % (tournament_name))
        conn.commit()
        return "%s is added" % tournament_name  
    
@app.route('/tournament', methods=['PUT', 'OPTIONS'])
@crossdomain(origin='*')
def edit_tournament():
    tournament_id = request.get_json().get('tournament_id', '')
    tournament_name = request.get_json().get('tournament_name', '')
    cursor.execute("UPDATE Tournament SET tournament_name = '%s' where id = '%d'" % (tournament_name, tournament_id))
    conn.commit()
    return "%s is updated!" % tournament_name 
   
@app.route('/getplayers', methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
def getplayers():
    # order_by = order by enten username eller display_name, maa sendes med GET'en fra clienten
        cursor.execute("select username, p.id, countrycode, display_rating, team_name, c.name as country from Player p LEFT JOIN Team t ON p.team_id = t.id LEFT JOIN Countries c ON p.countrycode = c.alpha_2") # ORDER BY username desc")# % (order_by))
        data = [dict(line) for line in [zip([column[0] for column in cursor.description], 
                                            row) for row in cursor.fetchall()]]
    
        print data
        return jsonify(data=data)


@app.route('/match', methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
def get_matches():
    cursor.execute("select m.id, m.match_id, tournament_id, team_1_id, team_2_id, winning_team_id, losing_team_id, FROM_UNIXTIME(match_time_start) as match_time_start, FROM_UNIXTIME(match_time_end) as match_time_end, w.team_name AS winning_team, l.team_name AS losing_team FROM Matches m LEFT JOIN Team w on m.winning_team_id = w.id LEFT JOIN Team l on m.losing_team_id = l.id order by m.id;")
    data = [dict(line) for line in [zip([column[0] for column in cursor.description], 
                                        row) for row in cursor.fetchall()]]

    return jsonify(data=data)

@app.route('/match', methods=['POST', 'OPTIONS'])
@crossdomain(origin='*')
def create_match():
    # tournament_id = request.get_json().get('tournament_id', '')
        time_start = request.get_json().get('match_time_start', '')
        time_end = request.get_json().get('match_time_end', '')
        team_1_id = request.get_json().get('team_1_id', '')
        team_2_id = request.get_json().get('team_2_id', '')
        winning_team_id = request.get_json().get('winning_team_id', '')
        losing_team_id = request.get_json().get('losing_team_id', '')
        tournament_id = request.get_json().get('tournament_id', '')
        cursor.execute("INSERT INTO Matches (tournament_id, team_1_id, team_2_id, winning_team_id, losing_team_id, match_time_start, match_time_end) VALUES ('%d', '%d', '%d', '%d', '%d', UNIX_TIMESTAMP('%s'), UNIX_TIMESTAMP('%s'))" % (tournament_id, team_1_id, team_2_id, winning_team_id, losing_team_id, '2014-05-14', '2014-05-14'))#time_start, time_end))
        conn.commit()
        cursor.execute("SELECT LAST_INSERT_ID()")
        match_id = cursor.fetchone()[0]
        eloCalc(match_id)
        return "match_id som blir sendt til kalkis esportrating: ", match_id; 

# NEEDS TO BE NOT 0
        #if(winning_team_id and losing_team_id != -1): 
            

#        return "Match is added!"

@app.route('/match', methods=['PUT', 'OPTIONS'])
@crossdomain(origin='*')
def update_match(match_id):
    #match_id = 1 #Faa tak i id'en til matchen det er snakk om
    time_start = request.get_json().get('time_start', '')
    time_end = request.get_json().get('time_end', '')
    team_1_id = request.get_json().get('team_1_id', '')
    team_2_id = request.get_json().get('team_2_id', '')
    winning_team_id = request.get_json().get('winning_team_id', '')
    losing_team_id = request.get_json().get('losing_team_id', '')
#    cursor.execute("UPDATE Matches SET team_1_id = '%d', team_2_id = '%d', winning_team_id = '%d', losing_team_id = '%d', match_time_start = UNIX_TIMESTAMP('%s'), match_time_end = UNIX_TIMESTAMP('%s')))" % (team_1_id, team_2_id, winning_team_id, losing_team_id, time_start, time_end))
#    if(winning_team_id and losing_team_id != null):
#        eloCalc(match_id)
#    conn.commit()
    cursor.execute("UPDATE Matches SET team_1_id = '%d', team_2_id = '%d', winning_team_id = '%d', losing_team_id = '%d', match_time_start = UNIX_TIMESTAMP('%s'), match_time_end = UNIX_TIMESTAMP('%s')) WHERE id = '%s')" % (team_1_id, team_2_id, winning_team_id, losing_team_id, time_start, time_end, match_id))
    conn.commit()    
    print "CHECK"
    check(match_id)
    print "ELO-CALC"
    eloCalc(match_id)
    return "Match is updated!"

@app.route('/match/<int:match_id>', methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
def get_match(match_id):
    cursor.execute("SELECT * FROM Matches WHERE id = '%d'" % (match_id))
    data = [dict(line) for line in [zip([column[0] for column in cursor.description], 
                                        row) for row in cursor.fetchall()]]
    return jsonify(data=data)

@app.route('/player_match', methods=['POST', 'OPTIONS'])
@crossdomain(origin='*')
def create_player_match():
    # tournament_id = request.get_json().get('tournament_id', '')
    match_id = request.get_json().get('match_id', '')
    player_id = request.get_json().get('player_id', '')
    team_id = request.get_json().get('team_id', '')
    cursor.execute("INSERT INTO Player_match (match_id, player_id, team_id) VALUES ('%d', '%d', '%d')" % (match_id, player_id, team_id))
    conn.commit()
    return "%d is added" % match_id  

@app.route('/countries', methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
def get_countries():
    cursor.execute("select * from Countries")
    data = [dict(line) for line in [zip([column[0] for column in cursor.description], 
                                        row) for row in cursor.fetchall()]]
    return jsonify(data=data)
    
    

#@app.route('/getplayers', methods=['GET', 'OPTIONS'])
#@crossdomain(origin='*')
#def getplayers():
#    cursor.execute("select username, display_rating, team_name from Player p, Team t WHERE p.team_id = t.id")
#    data = [dict(line) for line in [zip([column[0] for column in cursor.description], 
#                                        row) for row in cursor.fetchall()]]
#    return jsonify(data=data)
#HALLOHALLO
#api.add_resource(Tournament, '/tournament') #GET all tournaments, POST new torunament: '{"tournament_id":INT, "time_start":TIMESTAMP, "time_end":TIMESTAMP, "tournament_name":STRING}'
#api.add_resource(Team, '/team') #GET all teams, POST new team: '{"team_id":INT, "team_name":"STRING"}'
#api.add_resource(Player, '/player') #GET player by username: '{"username":"STRING"}', POST new player: '{"player_id":INT, "username":"STRING", "team_id":INT(has to already exist)}'
  
if __name__ == '__main__':
    app.run(host="0.0.0.0",
            port=int("5001"))