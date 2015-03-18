from flask import Flask, request, json, jsonify
from flask.ext.restful import Api, Resource, reqparse, fields, marshal
import MySQLdb

#acces-control-allow-origin
from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper

app = Flask(__name__)
api = Api(app)

from flask.ext.cors import CORS
cors = CORS(app) #added

try:
    conn = MySQLdb.connect(host="localhost", user="root", passwd="HenrietteIda", db="esport")
    cursor = conn.cursor()
    
except MySQLdb.Error, e:
    print "Error %d: %s" % (e.args[0], e.args[1])
    sys.exit(1)

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
        
@app.route('/player/<username>', methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
def get_player(username):
        print ("Hallohallo")
        #username = request.get_json().get('username', '')
        print ("Hallohalloigjen")
        print request.args.get('username')
        cursor.execute("SELECT username, display_rating FROM Player WHERE username = '%s'" % (username))
        data = [dict(line) for line in [zip([column[0] for column in cursor.description], 
                                            row) for row in cursor.fetchall()]]
        
        return jsonify(data=data)

@app.route('/player', methods=['POST', 'OPTIONS'])
@crossdomain(origin='*')
def create_player():
        player_id = request.get_json().get('player_id', '')
        print player_id
        username = request.get_json().get('username', '')
        team_id = request.get_json().get('team_id', '')
        cursor.execute("INSERT INTO Player VALUES ('%d', '%s', '%d', '%d', '%d')" % (player_id, username, 1200, 1200, team_id))
        conn.commit()
        return "%s is added" % username
    
@app.route('/team', methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
def get_teams():
        cursor.execute("SELECT * FROM Team")
        data = [dict(line) for line in [zip([column[0] for column in cursor.description], 
                                            row) for row in cursor.fetchall()]]
        
        return jsonify(data=data)

@app.route('/team', methods=['POST', 'OPTIONS'])
@crossdomain(origin='*')
def create_teams():
        team_id = request.get_json().get('team_id', '')
        team_name = request.get_json().get('team_name', '')
        cursor.execute("INSERT INTO Team VALUES ('%d', '%s')" % (team_id, team_name))
        conn.commit()
        return "%s is added" % team_name    

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
        tournament_id = request.get_json().get('tournament_id', '')
        time_start = request.get_json().get('time_start', '')
        time_end = request.get_json().get('time_end', '')
        tournament_name = request.get_json().get('tournament_name', '')
        cursor.execute("INSERT INTO Tournament VALUES ('%d', '%s', '%s', '%s')" % (tournament_id, time_start, time_end, tournament_name))
        conn.commit()
        return "%s is added" % tournament_name   
   
@app.route('/getplayers', methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
def getplayers():
    cursor.execute("select username, display_rating, team_name from Player p, Team t WHERE p.team_id = t.team_id")
    data = [dict(line) for line in [zip([column[0] for column in cursor.description], 
                                        row) for row in cursor.fetchall()]]
    return jsonify(data=data)

#api.add_resource(Tournament, '/tournament') #GET all tournaments, POST new torunament: '{"tournament_id":INT, "time_start":TIMESTAMP, "time_end":TIMESTAMP, "tournament_name":STRING}'
#api.add_resource(Team, '/team') #GET all teams, POST new team: '{"team_id":INT, "team_name":"STRING"}'
#api.add_resource(Player, '/player') #GET player by username: '{"username":"STRING"}', POST new player: '{"player_id":INT, "username":"STRING", "team_id":INT(has to already exist)}'

if __name__ == '__main__':
    app.run(host="0.0.0.0",
            port=int("5001"))