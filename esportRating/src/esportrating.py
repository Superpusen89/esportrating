from flask import Flask, request, json
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
    
    
    
    
    
class HelloWorld(Resource):
    def get(self):
        return 'Hello world'

#player_fields = {
 #   'player_id': fields.Integer,
  #  'username': fields.String,
   # 'team_id': fields.Integer
#}


class Player(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('player_id', type=int, location='json')
        self.reqparse.add_argument('username', type=str, location='json')
        self.reqparse.add_argument('team_id', type=int, location='json')
        super(Player, self).__init__()
        
    def get(self):
        cursor.execute("select * from Player") # where username = %s", (user_name))
        data = cursor.fetchall()
        return data
    
    def post(self):
        args = self.reqparse.parse_args()
        print args
        
        
class GetPlayers(Resource):
    def get(self):
        cursor.execute("select * from Player")
        data = cursor.fetchall()
        print data
            
        

api.add_resource(GetPlayers, '/getplayers')
api.add_resource(HelloWorld, '/')
api.add_resource(Player, '/getplayer')





cursor.execute("select * from Player")


if __name__ == '__main__':
    app.run(host="0.0.0.0",
        port=int("5001"))