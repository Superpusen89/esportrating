#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import MySQLdb
import datetime
from datetime import timedelta
from decimal import Decimal
from flask import Flask
from flask import current_app
from flask import jsonify
from flask import make_response
from flask import request
from flask.ext.restful import Api
from functools import update_wrapper
import math
import queries
import sys
import time

app = Flask(__name__)
api = Api(app)

from flask.ext.cors import CORS
cors = CORS(app) #added

try:
    conn = MySQLdb.connect(host="localhost", user="root", passwd="HenrietteIda", db="esportrating", use_unicode=True, charset="utf8")
    conn.autocommit(True)
    cursor = conn.cursor()
    
except MySQLdb.Error, e:
    print "Error %d: %s" % (e.args[0], e.args[1])
    sys.exit(1)



def getMonth():
    month = datetime.datetime.now().month
    cursor.execute(queries.q24)
    prevMonth = cursor.fetchone()[0]
    if month != prevMonth:
        cursor.execute(queries.q26 % [month])
        conn.commit()
        updateBaseRating()
    return 0

def orderRank():
    cursor.execute(queries.q28)
    data = cursor.fetchall()
    length = len(data)
    i = 1
    rank = 1
    for row in data:
        if i<length-1:
            if row[1] == data[i][1]: #Hvis begge har lik score
                if row[2] == data[i][2]:
                    cursor.execute(queries.q29, [rank, row[0]]) #Hvis begge har like mange matches
                else:
                    cursor.execute(queries.q29, [rank, row[0]]) #Hvis den forste har flere matches
                    rank += 1
            else:
                cursor.execute(queries.q29, [rank, row[0]]) #Naar den forste har fler points
                rank += 1
            i += 1
    cursor.execute(queries.q29, [rank, data[length-1][0]])

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
       
#def check(match_id):
#    cursor.execute("SELECT COUNT(points) FROM Player_match WHERE match_id = '%s'" % (match_id))
#    count = cursor.fetchone()[0]
#    if(count != 0):
#        resetDisplayRating(match_id)

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
            cursor.execute("UPDATE Player SET display_rating = '%s' WHERE id = '%d'" % (newDisplay_rating, player_id))
            conn.commit()
    

def eloCalc(match_id):
    getMonth()
    cursor.execute(queries.findAVG1, [match_id, match_id]) #finds losing team's average score
    B = float(cursor.fetchone()[0])
    cursor.execute(queries.findAVG2, [match_id, match_id]) #finds winning team's average score
    A = float(cursor.fetchone()[0])
    #Elo-rating formula
    Es = 1.0 / (1.0 + math.pow(10.0, ((B-A) / 400.0)))
    R = round(Decimal(15 * (1-Es)), 2) #winning team points
    cursor.execute(queries.findID1, [match_id, match_id]) #finds every participating player on winning team
    ID = cursor.fetchall()
    for row in ID: #for each player -> update points
        id = row[0]
        cursor.execute(queries.updatePoints, [R, match_id, id])
        conn.commit()
    R = -R #losing team points
    cursor.execute(queries.findID2, [match_id, match_id]) #finds every participating player on winning team
    ID = cursor.fetchall()
    for row in ID: #for each player -> update points
        id = row[0]
        cursor.execute(queries.updatePoints, [R, match_id, id])
        conn.commit()
    setDisplayRating(match_id) #run this method
    orderRank() #run this method
    

#def setDisplayRating(match_id):
#    cursor.execute("SELECT pm.points, p.id FROM Player_match pm, Player p WHERE match_id='%s' AND pm.player_id=p.id" % (match_id))
#    data = cursor.fetchall()
#    for row in data:
#        points = float(row[0])
#        player_id = float(row[1])
#        cursor.execute("SELECT display_rating FROM Player WHERE id = '%s'" % player_id)
#        display_rating = float(cursor.fetchone()[0])
#        newDisplay_rating = display_rating + points
#        cursor.execute("UPDATE Player SET display_rating = '%s' WHERE id = '%d'" % (newDisplay_rating, player_id))
#        conn.commit()



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


@app.route('/player/<int:player_id>', methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
def get_player(player_id):
    cursor.execute("SELECT avatar, p.id, p.id as player_id, countrycode, username, realname, rank, display_rating, base_rating, team_name, COUNT(pm.match_id) as count, p.team_id, c.name as country FROM Player p LEFT JOIN Team t on p.team_id = t.id LEFT JOIN Countries c ON p.countrycode = c.alpha_2 LEFT JOIN Player_match pm ON p.id = pm.player_id WHERE p.id = '%d'" % (player_id))
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
def add_player():
    username = request.get_json().get('username', '')
    team_id = request.get_json().get('team_id', '')
    avatar = request.get_json().get('avatar', '')
    real_name = request.get_json().get('real_name', '')
    country = request.get_json().get('country', '')
        
    if len(country) != 2:
        country = 'null';
        
    if len(str(team_id)) == 0:
        cursor.execute("INSERT INTO Player (username, base_rating, display_rating, avatar, realname, countrycode) VALUES (%s, %s, %s, %s, %s, %s)", [username, 1200, 1200, avatar, real_name, country]) 
    elif len(str(team_id)) != 0:    
        cursor.execute("INSERT INTO Player (username, base_rating, display_rating, team_id, avatar, realname, countrycode) VALUES (%s, %s, %s, %s, %s, %s, %s)", [username, 1200, 1200, team_id, avatar, real_name, country])
    
    conn.commit()
    return "%s is added" % username
        

@app.route('/player', methods=['PUT', 'OPTIONS'])
@crossdomain(origin='*')
def edit_player():
    player_id = request.get_json().get('player_id', '')
    username = request.get_json().get('username', '')
    team_id = request.get_json().get('team_id', '')
    avatar = request.get_json().get('avatar', '')
    realname = request.get_json().get('realname', '')
    country = request.get_json().get('countrycode', '')
    
    if team_id == None:
        cursor.execute("UPDATE Player SET username = '%s', avatar = '%s', realname = '%s', countrycode = '%s' where id = '%d'" % (username, avatar, realname, country, player_id))
    elif team_id != None:
        cursor.execute("UPDATE Player SET username = '%s', team_id = '%d', avatar = '%s', realname = '%s', countrycode = '%s' where id = '%d'" % (username, team_id, avatar, realname, country, player_id))
        
    
    conn.commit()
    return "%s is updated!" % username

@app.route('/team/<int:team_id>', methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
def get_team(team_id):
    cursor.execute("SELECT t.id, t.team_id, t.team_name, COUNT(t.id) as count FROM Team t LEFT JOIN Matches m ON (t.id = team_1_id) OR (t.id = m.team_2_id) WHERE t.id = '%d'" % (team_id))
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
    cursor.execute("SELECT t.id, t.team_id, t.team_name, COUNT(t.id) as count FROM Team t LEFT JOIN Matches m ON (t.id = team_1_id) OR (t.id = m.team_2_id) GROUP BY t.id")
#    cat = '哈哈'
    data = [dict(line) for line in [zip([column[0] for column in cursor.description], 
                                        row) for row in cursor.fetchall()]]
        
    return jsonify(data=data)

@app.route('/team', methods=['POST', 'OPTIONS'])
@crossdomain(origin='*')
def add_team():
    team_name = request.get_json().get('team_name', '')
    cursor.execute('INSERT INTO Team (team_name) VALUES (%s)', [team_name])
    conn.commit()

    cursor.execute("SELECT LAST_INSERT_ID()")
    team_id = cursor.fetchone()[0]
    return "%d" % team_id; 
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
def view_tournaments():
    cursor.execute("select * from Tournament")
    data = [dict(line) for line in [zip([column[0] for column in cursor.description], 
                                        row) for row in cursor.fetchall()]]
    return jsonify(data=data)

@app.route('/tournament', methods=['POST', 'OPTIONS'])
@crossdomain(origin='*')
def add_tournament():
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
def view_ranking_list():
    cursor.execute("select username, rank, p.id, p.id as player_id, countrycode, display_rating, p.team_id, COUNT(pm.match_id) as count, team_name, c.name as country from Player p LEFT JOIN Team t ON p.team_id = t.id LEFT JOIN Countries c ON p.countrycode = c.alpha_2 LEFT JOIN Player_match pm ON p.id = pm.player_id group by p.id order by rank asc") # ORDER BY username desc")# % (order_by))
    data = [dict(line) for line in [zip([column[0] for column in cursor.description], 
                                        row) for row in cursor.fetchall()]]

    return jsonify(data=data)

@app.route('/match', methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
def get_matches():
    cursor.execute("select m.id, m.match_id, m.tournament_id, team_1_id, team_2_id, winning_team_id, losing_team_id, FROM_UNIXTIME(match_time_start) as match_time_start, FROM_UNIXTIME(match_time_end) as match_time_end, w.team_name AS winning_team, l.team_name AS losing_team, one.team_name AS team_1_name, two.team_name AS team_2_name, t.tournament_name FROM Matches m JOIN Tournament t on m.tournament_id = t.id LEFT JOIN Team w on m.winning_team_id = w.id LEFT JOIN Team l on m.losing_team_id = l.id LEFT JOIN Team one ON m.team_1_id = one.id LEFT JOIN Team two ON m.team_2_id = two.id order by m.match_time_start desc")
    data = [dict(line) for line in [zip([column[0] for column in cursor.description], 
                                        row) for row in cursor.fetchall()]]
    return jsonify(data=data)

@app.route('/match', methods=['POST', 'OPTIONS'])
@crossdomain(origin='*')
def add_match():
    time_start = request.get_json().get('match_time_start', '')
    time_end = request.get_json().get('match_time_end', '')
    team_1_id = request.get_json().get('team_1_id', '')
    team_2_id = request.get_json().get('team_2_id', '')
    winning_team_id = request.get_json().get('winning_team_id', '')
    losing_team_id = request.get_json().get('losing_team_id', '')
    tournament_id = request.get_json().get('tournament_id', '')
    cursor.execute("INSERT INTO Matches (tournament_id, team_1_id, team_2_id, winning_team_id, losing_team_id, match_time_start, match_time_end) VALUES ('%d', '%d', '%d', '%d', '%d', UNIX_TIMESTAMP('%s'), UNIX_TIMESTAMP('%s'))" % (tournament_id, team_1_id, team_2_id, winning_team_id, losing_team_id, time_start, time_end))
    conn.commit()
    
    cursor.execute("SELECT LAST_INSERT_ID()")
    match_id = cursor.fetchone()[0]
    return "Match %d is added" % match_id; 




@app.route('/match', methods=['PUT', 'OPTIONS'])
@crossdomain(origin='*')
def update_match():

    match_id = request.get_json().get('id', '')
    time_start = request.get_json().get('match_time_start', '')
    time_end = request.get_json().get('match_time_end', '')
    team_1_id = request.get_json().get('team_1_id', '')
    team_2_id = request.get_json().get('team_2_id', '')
    winning_team_id = request.get_json().get('winning_team_id', '')
    losing_team_id = request.get_json().get('losing_team_id', '')
    tournament_id = request.get_json().get('tournament_id', '')
  
    cursor.execute("UPDATE Matches SET team_1_id = '%d', team_2_id = '%d', winning_team_id = '%d', losing_team_id = '%d', match_time_start = UNIX_TIMESTAMP('%s'), match_time_end = UNIX_TIMESTAMP('%s'), tournament_id = '%d' WHERE id = '%d'" % (team_1_id, team_2_id, winning_team_id, losing_team_id, time_start, time_end, tournament_id, match_id))
    conn.commit()

    return "Data sent to Elo-calc: %d " % match_id

@app.route('/match/<int:match_id>', methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
def get_match(match_id):
    cursor.execute("select m.id, m.match_id, m.tournament_id, team_1_id, team_2_id, winning_team_id, losing_team_id, FROM_UNIXTIME(match_time_start) as match_time_start, FROM_UNIXTIME(match_time_start, '%%Y-%%m-%%dT%%H:%%i') as f_time_start, FROM_UNIXTIME(match_time_end) as match_time_end, FROM_UNIXTIME(match_time_end, '%%Y-%%m-%%dT%%H:%%i') as f_time_end, w.team_name AS winning_team, l.team_name AS losing_team, one.team_name AS team_1_name, two.team_name AS team_2_name, t.tournament_name FROM Matches m JOIN Tournament t on m.tournament_id = t.id LEFT JOIN Team w on m.winning_team_id = w.id LEFT JOIN Team l on m.losing_team_id = l.id LEFT JOIN Team one on m.team_1_id = one.id LEFT JOIN Team two on m.team_2_id = two.id WHERE m.id = '%d'" % (match_id))
    data = [dict(line) for line in [zip([column[0] for column in cursor.description], 
                                        row) for row in cursor.fetchall()]]
    return jsonify(data=data)

@app.route('/match_tournament/<int:tournament_id>', methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
def get_matches_tournament(tournament_id):
    cursor.execute("SELECT m.id, team_1_id, team_2_id, FROM_UNIXTIME(match_time_start, '%%a %%b %%e. %%Y %%H:%%i') AS match_time_start, one.team_name AS team_1_name, two.team_name AS team_2_name FROM Matches m LEFT JOIN Team one ON m.team_1_id = one.id LEFT JOIN Team two ON m.team_2_id = two.id WHERE tournament_id = '%d'" % (tournament_id))
    data = [dict(line) for line in [zip([column[0] for column in cursor.description], 
                                        row) for row in cursor.fetchall()]]
    return jsonify(data=data)

@app.route('/player_match', methods=['POST', 'OPTIONS'])
@crossdomain(origin='*')
def add_player_match():
    
    match_id = request.get_json().get('match_id', '')
    player_id = request.get_json().get('player_id', '')
    team_id = request.get_json().get('team_id', '')
    
    cursor.execute("INSERT INTO Player_match (match_id, player_id, team_id) VALUES ('%d', '%d', '%d')" % (match_id, player_id, team_id))
    conn.commit()
    
    return "%d is added" % match_id  

@app.route('/player_match/<int:match_id>,<int:team_id>', methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
def get_player_match(match_id, team_id):
    cursor.execute("select pm.match_id, pm.team_id, pm.player_id, p.username from Player_match pm join Player p on pm.player_id = p.id where pm.match_id = '%d' and pm.team_id= '%d'" % (match_id, team_id))
    data = [dict(line) for line in [zip([column[0] for column in cursor.description], 
                                        row) for row in cursor.fetchall()]]
    return jsonify(data=data)

@app.route('/delete_player_match', methods=['PUT', 'OPTIONS'])
@crossdomain(origin='*')
def delete_player_match():
    match_id = request.get_json().get('match_id', '')

    print "DELETE match_id ", match_id, "type: ", type(match_id)
    
    cursor.execute("DELETE FROM Player_match where match_id = '%d'" % (match_id))
    conn.commit()
    return "%d is deleted" % match_id 

@app.route('/player_match', methods=['PUT', 'OPTIONS'])
@crossdomain(origin='*')
def update_player_match():

    match_id = request.get_json().get('match_id', '')
    old_team_id = request.get_json().get('old_team_id', '')
    new_team_id = request.get_json().get('new_team_id', '')
    old_player_id = request.get_json().get('old_player_id', '')
    new_player_id = request.get_json().get('new_player_id', '')
  
    cursor.execute("UPDATE Player_match SET player_id = '%d', team_id = '%d' WHERE player_id = '%d' AND team_id = '%d' AND match_id = '%d'" % (new_player_id, new_team_id, old_player_id, old_team_id, match_id))
    conn.commit()   

    return "Successfully updated match %d " % match_id

@app.route('/calculate', methods=['PUT', 'OPTIONS'])
@crossdomain(origin='*')
def calculate():
    match_id = request.get_json().get('match_id', '');
    print "CALCULATE Match id: ", match_id, " Type: ", type(match_id)
    eloCalc(match_id)
    return "Successfully calculated match %d" % match_id

@app.route('/resetELO', methods=['PUT', 'OPTIONS'])
@crossdomain(origin='*')
def reset():
    match_id = request.get_json().get('match_id', '');
    print "RESET Match id: ", match_id, " Type: ", type(match_id)
    resetDisplayRating(match_id)
    return "Successfully resat match %d" % match_id    

@app.route('/countries', methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
def get_countries():
    cursor.execute("select * from Countries")
    data = [dict(line) for line in [zip([column[0] for column in cursor.description], 
                                        row) for row in cursor.fetchall()]]
    return jsonify(data=data)
    
 
if __name__ == '__main__':
    app.run(host="0.0.0.0",
            port=int("5001"))