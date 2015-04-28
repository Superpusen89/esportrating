q1 = "SELECT EXISTS(SELECT id FROM Tournament WHERE tournament_id = '%d')"
q2 = "INSERT INTO Tournament (tournament_id, tournament_name) VALUES ('%d', '%s')"
q3 = "SELECT EXISTS(SELECT id FROM Team WHERE team_id = '%d')"
q4 = "INSERT INTO Team (team_id, team_name) VALUES ('%d', '%s')"
q5 = "SELECT EXISTS(SELECT id FROM Player WHERE player_id = '%d')"
q6 = "INSERT INTO Player (player_id, username, base_rating, display_rating, team_id, avatar, realname, countrycode) VALUES ('%d', '%s', '%d', '%d', (SELECT id from Team WHERE team_id = '%d'), '%s', '%s', '%s')"
q7 = "SELECT EXISTS(SELECT id FROM Matches WHERE match_id = '%d')"
q8 = "INSERT INTO Matches (match_id, tournament_id, winning_team_id, losing_team_id, match_time_start, match_time_end) VALUES ('%d', (SELECT id FROM Tournament WHERE tournament_id = '%d'), '%d', '%d', '%d', '%d')"
q9 = "INSERT INTO Matches (match_id, tournament_id, winning_team_id, losing_team_id, match_time_start, match_time_end) VALUES ('%d', (SELECT id FROM Tournament WHERE tournament_id = '%d'), '%d', '%d', '%d', '%d')"
q10 = "SELECT EXISTS(SELECT * FROM Player_match WHERE match_id = (SELECT id FROM Matches WHERE match_id = '%d') AND player_id = (SELECT id FROM Player WHERE player_id = '%d'))"
q11 = "INSERT INTO Player_match (match_id, player_id, team_id) VALUES ((SELECT id FROM Matches WHERE match_id = '%d'), (SELECT id FROM Player WHERE player_id = '%d'), '%d')"


