from flask import Flask
from flask.ext.restful import Api, Resource
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

class GetPlayers(Resource):
    def get(self):
        cursor.execute("select * from Player")
        data = cursor.fetchall()
        print data
            
        

api.add_resource(GetPlayers, '/getplayers')
api.add_resource(HelloWorld, '/')



cursor.execute("select * from Player")


if __name__ == '__main__':
    app.run(host="0.0.0.0",
        port=int("5001"))