q1 = 'SELECT EXISTS(SELECT id FROM Tournament WHERE tournament_id = %s)'
q2 = 'INSERT INTO Tournament (tournament_id, tournament_name) VALUES (%s, %s)'
q3 = "SELECT EXISTS(SELECT id FROM Team WHERE team_id = %s)"
q4 = "INSERT INTO Team (team_id, team_name) VALUES (%s, %s)"
q5 = "SELECT EXISTS(SELECT id FROM Player WHERE player_id = %s)"
q6 = "INSERT INTO Player (player_id, username, base_rating, display_rating, team_id, avatar, realname, countrycode) VALUES (%s, %s, %s, %s, (SELECT id from Team WHERE team_id = %s), %s, %s, %s)"
q7 = "SELECT EXISTS(SELECT id FROM Matches WHERE match_id = %s)"
q8 = "INSERT INTO Matches (match_id, tournament_id, team_1_id, team_2_id, winning_team_id, losing_team_id, match_time_start, match_time_end) VALUES (%s, (SELECT id FROM Tournament WHERE tournament_id = %s), (SELECT id FROM Team WHERE team_id=%s), (SELECT id FROM Team WHERE team_id=%s), (SELECT id FROM Team WHERE team_id=%s), (SELECT id FROM Team WHERE team_id=%s), %s, %s)"
q9 = "INSERT INTO Matches (match_id, tournament_id, team_1_id, team_2_id, winning_team_id, losing_team_id, match_time_start, match_time_end) VALUES (%s, (SELECT id FROM Tournament WHERE tournament_id = %s), (SELECT id FROM Team WHERE team_id=%s), (SELECT id FROM Team WHERE team_id=%s), (SELECT id FROM Team WHERE team_id=%s), (SELECT id FROM Team WHERE team_id=%s), %s, %s)"
q10 = "SELECT EXISTS(SELECT * FROM Player_match WHERE match_id = (SELECT id FROM Matches WHERE match_id = %s) AND player_id = (SELECT id FROM Player WHERE player_id = %s))"
q11 = "INSERT INTO Player_match (match_id, player_id, team_id) VALUES ((SELECT id FROM Matches WHERE match_id = %s), (SELECT id FROM Player WHERE player_id = %s), (SELECT id FROM Team WHERE team_id = %s))"
q12 = "SELECT username, player_id FROM Player"
q13 = "UPDATE Player SET username = %s WHERE player_id = %s"
q14 = "SELECT team_id, team_name FROM Team"
q15 = "UPDATE Team SET team_name = %s WHERE team_id = %s"
q16 = "SELECT EXISTS(SELECT * FROM Player WHERE player_id = %s)"
q17 = "INSERT INTO Player (player_id, username, base_rating, display_rating, avatar, realname, countrycode) VALUES (%s, %s, %s, %s, %s, %s, %s)"
q18 = "SELECT COUNT(id) FROM Matches WHERE tournament_id = (SELECT id from Tournament WHERE tournament_id = %s)"
q19 = "SELECT match_id FROM Matches WHERE id = (SELECT MAX(id) FROM Matches WHERE tournament_id = (SELECT id FROM Tournament WHERE tournament_id=%s))"
q20 = "DELETE FROM Matches WHERE match_id = %s"
q21 = "DELETE FROM Player_match WHERE match_id = (SELECT id FROM Matches WHERE match_id = %s)"
q22 = "SELECT COUNT(id) FROM Matches WHERE tournament_id = (SELECT id FROM Tournament WHERE tournament_id = %s);"
q23 = "UPDATE Player SET base_rating=display_rating"
q24 = "SELECT current_month FROM Game_period"
q25 = "INSERT INTO Game_period VALUES (%s)"
q26 = "UPDATE Game_period SET current_month = %s"
q27 = "SELECT match_id, FROM_UNIXTIME(match_time_start, \"%m\") FROM Matches ORDER BY match_time_start"
q28 = "SELECT p.id, p.display_rating, (SELECT COUNT(match_id) FROM Player_match WHERE player_id = p.id) AS num_match FROM Player p JOIN Player_match pm ON p.id = pm.player_id GROUP BY p.id ORDER BY display_rating desc, num_match desc"
q29 = "UPDATE Player SET rank = %s WHERE id = %s"


#ELO-calc
findAVG = "SELECT AVG(base_rating) FROM Player WHERE id= ANY (SELECT player_id FROM Player_match WHERE match_id = %s) AND team_id=(SELECT %s FROM Matches WHERE id=%s)"
findAVGnew = "SELECT AVG(base_rating) FROM Player WHERE id= ANY (SELECT player_id FROM Player_match WHERE match_id = %s AND team_id=(SELECT %s FROM Matches WHERE id=%s)"
findID = "SELECT id FROM Player WHERE id= ANY (SELECT player_id FROM Player_match WHERE match_id = %s) AND team_id=(SELECT %s FROM Matches WHERE id=%s)"
updatePoints = "UPDATE Player_match set points = %s WHERE match_id = (SELECT id FROM Matches WHERE match_id = %s) AND player_id = %s"

findAVG2 = "SELECT AVG(base_rating) FROM Player WHERE id=ANY(SELECT player_id FROM Player_match WHERE match_id = (SELECT id FROM Matches WHERE match_id = %s) AND team_id = (SELECT %s FROM Matches WHERE match_id = %s))"
findAVG3 = "SELECT AVG(base_rating) FROM Player WHERE id=ANY(SELECT player_id FROM Player_match WHERE match_id = (SELECT id FROM Matches WHERE match_id = %s) AND team_id = (SELECT losing_team_id FROM Matches WHERE match_id = %s))"
findAVG4 = "SELECT AVG(base_rating) FROM Player WHERE id=ANY(SELECT player_id FROM Player_match WHERE match_id = (SELECT id FROM Matches WHERE match_id = %s) AND team_id = (SELECT winning_team_id FROM Matches WHERE match_id = %s))"
findID1 = "SELECT id FROM Player WHERE id= ANY (SELECT player_id FROM Player_match WHERE match_id = (SELECT id FROM Matches WHERE match_id = %s) AND team_id = (SELECT winning_team_id FROM Matches WHERE match_id = %s))"
findID2 = "SELECT id FROM Player WHERE id= ANY (SELECT player_id FROM Player_match WHERE match_id = (SELECT id FROM Matches WHERE match_id = %s) AND team_id = (SELECT losing_team_id FROM Matches WHERE match_id = %s))"

#"SELECT AVG(base_rating) FROM Player WHERE id=ANY(SELECT player_id FROM Player_match WHERE match_id = (SELECT id FROM Matches WHERE match_id = 37626434) AND team_id = (SELECT losing_team_id FROM Matches WHERE match_id=37626434))"



