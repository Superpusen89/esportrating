# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "ida"
__date__ = "$03/02/2015 12:28:04 AM$"

from flask import Flask, render_template, request
import urllib, json
from team import Team

leagues = []
legends = []
players = []
testing = []

#find leagues
url = "http://api.steampowered.com/IDOTA2Match_205790/GetLeagueListing/v0001/?key=C60B2F253D948B27317D3EE293EE04ED"
json_obj = urllib.urlopen(url).read()
readable_json = json.loads(json_obj)

for l in readable_json['result']['leagues']:
    leagues.append(l['name'])

#find teams
url_legends = "http://api.steampowered.com/IDOTA2Match_570/GetTeamInfoByTeamID/v0001/?key=C60B2F253D948B27317D3EE293EE04ED"
json_obj_legends = urllib.urlopen(url_legends).read()
readable_json_legends = json.loads(json_obj_legends)

for leg in readable_json_legends['result']['teams']:
    #legends.append([leg['team_id'], leg['name']])
    legends.append(leg['name'])
    
#player stats
url_players = "http://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/v0001/?key=C60B2F253D948B27317D3EE293EE04ED&match_id=1169215228"
json_obj_players = urllib.urlopen(url_players).read()
readable_json_players = json.loads(json_obj_players)

for p in readable_json_players['result']['players']:
        players.append(p['account_id'])
        #players.append(Team(p['account_id'], p['kills']))
        #name = p['account_id']
        #id = p['kills']
        #testing.append(Team(name, id))
        
testing.append(Team('Jacob', '1'))
testing.append(Team('One', '0'))
name = 'building'
id = '2'
testing.append(Team(name, id))
#print t
#print t.name + '\n' + t.number


#STUFF
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('hello.html', items=leagues) 

@app.route('/buttons', methods=['POST'])
def button_handler():
    if 'leagues' in request.form:
        return render_template('hello.html', items=leagues)
    elif 'teams' in request.form:
        return render_template('hello.html', items=legends)
    elif 'players' in request.form:
        return render_template('hello.html', items=players)
    elif 'test' in request.form:
        return render_template('hello.html', items=testing)
    else: 
        return 'Error'

if __name__ == "__main__":
    app.run()