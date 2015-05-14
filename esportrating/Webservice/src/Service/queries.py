# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.


#Elo-calc
#findAVG = "SELECT AVG(base_rating) FROM Player WHERE id= ANY (SELECT player_id FROM Player_match WHERE match_id = '%s') AND team_id=(SELECT %s FROM Matches WHERE id='%s')"
#findAVGnew = "SELECT AVG(base_rating) FROM Player WHERE id= ANY (SELECT player_id FROM Player_match WHERE match_id = '%s' AND team_id=(SELECT %s FROM Matches WHERE id='%s')"
#findID = "SELECT id FROM Player WHERE id= ANY (SELECT player_id FROM Player_match WHERE match_id = '%s') AND team_id=(SELECT %s FROM Matches WHERE id='%s')"
#updatePoints = "UPDATE Player_match set points = '%s' WHERE match_id = '%s' AND player_id = '%d'"


findAVG = "SELECT AVG(base_rating) FROM Player WHERE id= ANY (SELECT player_id FROM Player_match WHERE match_id = %s) AND team_id=(SELECT %s FROM Matches WHERE id=%s)"
findAVGnew = "SELECT AVG(base_rating) FROM Player WHERE id= ANY (SELECT player_id FROM Player_match WHERE match_id = %s AND team_id=(SELECT %s FROM Matches WHERE id=%s)"
findID = "SELECT id FROM Player WHERE id= ANY (SELECT player_id FROM Player_match WHERE match_id = %s) AND team_id=(SELECT %s FROM Matches WHERE id=%s)"
updatePoints = "UPDATE Player_match set points = %s WHERE match_id = (SELECT id FROM Matches WHERE match_id = %s) AND player_id = %s"

findAVG1 = "SELECT AVG(base_rating) FROM Player WHERE id=ANY(SELECT player_id FROM Player_match WHERE match_id = (SELECT id FROM Matches WHERE match_id = %s) AND team_id = (SELECT losing_team_id FROM Matches WHERE match_id = %s))"
findAVG2 = "SELECT AVG(base_rating) FROM Player WHERE id=ANY(SELECT player_id FROM Player_match WHERE match_id = (SELECT id FROM Matches WHERE match_id = %s) AND team_id = (SELECT winning_team_id FROM Matches WHERE match_id = %s))"
findID1 = "SELECT id FROM Player WHERE id= ANY (SELECT player_id FROM Player_match WHERE match_id = (SELECT id FROM Matches WHERE match_id = %s) AND team_id = (SELECT winning_team_id FROM Matches WHERE match_id = %s))"
findID2 = "SELECT id FROM Player WHERE id= ANY (SELECT player_id FROM Player_match WHERE match_id = (SELECT id FROM Matches WHERE match_id = %s) AND team_id = (SELECT losing_team_id FROM Matches WHERE match_id = %s))"

#findAVG2 = "SELECT AVG(base_rating) FROM Player WHERE id=ANY(SELECT player_id FROM Player_match WHERE match_id = (SELECT id FROM Matches WHERE match_id = %s) AND team_id = (SELECT %s FROM Matches WHERE match_id=%s))"
insertTeam = "INSERT INTO Team (team_name) VALUES (%s)"

q24 = "SELECT current_month FROM Game_period"
q26 = "UPDATE Game_period SET current_month = %s"


def databaseConn():
    try:
        conn = MySQLdb.connect(host="localhost", user="root", passwd="HenrietteIda", db="esportrating", use_unicode=True, charset="utf8")
        conn.autocommit(True)
        cursor = conn.cursor()

    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)
        
    return cursor