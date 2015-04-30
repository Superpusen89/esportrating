q1 = 'SELECT EXISTS(SELECT id FROM Tournament WHERE tournament_id = %s)'
q2 = 'INSERT INTO Tournament (tournament_id, tournament_name) VALUES (%s, %s)'
q3 = "SELECT EXISTS(SELECT id FROM Team WHERE team_id = %s)"
q4 = "INSERT INTO Team (team_id, team_name) VALUES (%s, %s)"
q5 = "SELECT EXISTS(SELECT id FROM Player WHERE player_id = %s)"
q6 = "INSERT INTO Player (player_id, username, base_rating, display_rating, team_id, avatar, realname, countrycode) VALUES (%s, %s, %s, %s, (SELECT id from Team WHERE team_id = %s), %s, %s, %s)"
q7 = "SELECT EXISTS(SELECT id FROM Matches WHERE match_id = %s)"
q8 = "INSERT INTO Matches (match_id, tournament_id, winning_team_id, losing_team_id, match_time_start, match_time_end) VALUES (%s, (SELECT id FROM Tournament WHERE tournament_id = %s), %s, %s, %s, %s)"
q9 = "INSERT INTO Matches (match_id, tournament_id, winning_team_id, losing_team_id, match_time_start, match_time_end) VALUES (%s, (SELECT id FROM Tournament WHERE tournament_id = %s), %s, %s, %s, %s)"
q10 = "SELECT EXISTS(SELECT * FROM Player_match WHERE match_id = (SELECT id FROM Matches WHERE match_id = %s) AND player_id = (SELECT id FROM Player WHERE player_id = %s))"
q11 = "INSERT INTO Player_match (match_id, player_id, team_id) VALUES ((SELECT id FROM Matches WHERE match_id = %s), (SELECT id FROM Player WHERE player_id = %s), %s)"
q12 = "SELECT username, player_id FROM Player"
q13 = "UPDATE Player SET username = %s WHERE player_id = %s"
q14 = "SELECT team_id, team_name FROM Team"
q15 = "UPDATE Team SET team_name = %s WHERE team_id = %s"
q16 = "SELECT EXISTS(SELECT * FROM Player WHERE player_id = %s)"
q17 = "INSERT INTO Player (player_id, username, base_rating, display_rating, avatar, realname, countrycode) VALUES (%s, %s, %s, %s, %s, %s, %s)"




