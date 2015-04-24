# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.


#Elo-calc
findAVG = "SELECT AVG(base_rating) FROM Player WHERE id= ANY (SELECT player_id FROM Player_match WHERE match_id = '%s') AND team_id=(SELECT %s FROM Matches WHERE id='%s')"
findID = "SELECT id FROM Player WHERE id= ANY (SELECT player_id FROM Player_match WHERE match_id = '%s') AND team_id=(SELECT %s FROM Matches WHERE id='%s')"
updatePoints = "UPDATE Player_match set points = '%s' WHERE match_id = '%s' AND player_id = '%d'"