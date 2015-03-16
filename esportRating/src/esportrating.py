from flask import Flask, request, json, jsonify
from flask.ext.restful import Api, Resource, reqparse, fields, marshal
import MySQLdb

app = Flask(__name__)
api = Api(app)

try:
    conn = MySQLdb.connect(host="localhost", user="root", passwd="HenrietteIda", db="esport")
    cursor = conn.cursor()
    
except MySQLdb.Error, e:
    print "Error %d: %s" % (e.args[0], e.args[1])
    sys.exit(1)


class Player(Resource):    
    def get(self):
        user_name = request.get_json().get('user_name', '')
        cursor.execute("select username, display_rating from Player where username = '%s'", (user_name))
        data = cursor.fetchall()
        return jsonify(data = data)
    
    def post(self):
        player_id = request.get_json().get('player_id', '')
        username = request.get_json().get('username', '')
        team_id = request.get_json().get('team_id', '')
        cursor.execute("INSERT INTO Player VALUES ('%d', '%s', '%d', '%d', '%d')" % (player_id, username, 1200, 1200, team_id))
        conn.commit()
        return "%s is added" % username
    

class Team(Resource):
    def get(self): #Returns all teams
        cursor.execute("SELECT * FROM Team")
        data = cursor.fetchall()
        print data
        return jsonify(data = data)
    
    def post(self):
        team_id = request.get_json().get('team_id', '')
        team_name = request.get_json().get('team_name', '')
        cursor.execute("INSERT INTO Team VALUES ('%d', '%s')" % (team_id, team_name))
        conn.commit()
        return "%s is added" % team_name
              
        
class Tournament(Resource):
    def get(self):
        cursor.execute("select * from Tournament")
        data = cursor.fetchall()
        print data
        return jsonify(data = data)
    
    def post(self):
        tournament_id = request.get_json().get('tournament_id', '')
        time_start = request.get_json().get('time_start', '')
        time_end = request.get_json().get('time_end', '')
        tournament_name = request.get_json().get('tournament_name', '')
        cursor.execute("INSERT INTO Tournament VALUES ('%d', '%s', '%s', '%s')" % (tournament_id, time_start, time_end, tournament_name))
        conn.commit()
        return "%s is added" % tournament_name
        
      

class GetPlayers(Resource):
    def get(self):
        cursor.execute("select username, display_rating, team_name from Player p, Team t WHERE p.team_id = t.team_id")
        data = cursor.fetchall()
        data = jsonify(data = data)       
        print data
        return data
   


api.add_resource(GetPlayers, '/getplayers') #GET all players
api.add_resource(Tournament, '/tournament') #GET all tournaments, POST new torunament: '{"tournament_id":INT, "time_start":TIMESTAMP, "time_end":TIMESTAMP, "tournament_name":STRING}'
api.add_resource(Team, '/team') #GET all teams, POST new team: '{"team_id":INT, "team_name":"STRING"}'
api.add_resource(Player, '/player') #GET player by username: '{"username":"STRING"}', POST new player: '{"player_id":INT, "username":"STRING", "team_id":INT(has to already exist)}'



if __name__ == '__main__':
    app.run(host="0.0.0.0",
        port=int("5001"))