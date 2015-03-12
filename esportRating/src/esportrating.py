from flask import Flask, request, json, jsonify
from flask.ext.restful import Api, Resource, reqparse, fields, marshal
import MySQLdb

app = Flask(__name__)
api = Api(app)

try:
    conn = MySQLdb.connect(host="localhost", user="root", passwd="HenrietteIda", db="esportrating")
    cursor = conn.cursor()
    
except MySQLdb.Error, e:
    print "Error %d: %s" % (e.args[0], e.args[1])
    sys.exit(1)


class Player(Resource):    
    def get(self):
        user_name = request.get_json().get('user_name', '')
        print user_name #bare for testing
        cursor.execute("select * from Player where username = %s", (user_name))
        data = cursor.fetchall()
        return data
    
    def post(self):
        player_id = request.get_json().get('player_id', '')
        username = request.get_json().get('username', '')
        team_id = request.get_json().get('team_id', '')
        cursor.execute("INSERT INTO Player VALUES ('%d', '%s', '%d', '%d', '%d')" % (player_id, username, 1200, 1200, team_id))
        conn.commit()
        return "%s is added" % username
        
        
class GetPlayers(Resource):
    def get(self):
        cursor.execute("select * from Player")
        data = cursor.fetchall()
        print data
            
    def post(self):
        print "Hallohallo"

api.add_resource(GetPlayers, '/getplayers') #Get all players
api.add_resource(Player, '/player') #Get player by username: '{"username":"STRING"}', POST new player: '{"player_id":INT, "username":"STRING", "team_id":INT(has to already exist)}'


if __name__ == '__main__':
    app.run(host="0.0.0.0",
        port=int("5001"))