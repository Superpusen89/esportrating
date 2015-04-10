
DROP TABLE User_profile;
DROP TABLE Tournament;
DROP TABLE Team;
DROP TABLE Player_match;
DROP TABLE Player;
DROP TABLE Matches;



CREATE TABLE Team
(
    id INTEGER NOT NULL AUTO_INCREMENT, 
    team_id INTEGER,
    team_name CHAR(80),
    PRIMARY KEY (id)
);

CREATE TABLE Player
(
    id INTEGER NOT NULL AUTO_INCREMENT,
    player_id INTEGER,
    username CHAR(80),
    base_rating INTEGER,
    display_rating INTEGER,
    team_id INTEGER,
    PRIMARY KEY (id),
    FOREIGN KEY (team_id) REFERENCES Team(id)
);

CREATE TABLE Tournament
(
    id INTEGER NOT NULL AUTO_INCREMENT,
    tournament_id INTEGER,
    time_start TIMESTAMP,
    time_end TIMESTAMP,
    tournament_name CHAR(80),
    PRIMARY KEY (id)
);

CREATE TABLE Matches
(
    id INTEGER NOT NULL AUTO_INCREMENT,
    match_id INTEGER,
    tournament_id INTEGER,
    winning_team_id INTEGER NOT NULL,
    losing_team_id INTEGER NOT NULL,
    match_time_start TIMESTAMP,
    match_time_end TIMESTAMP,
    PRIMARY KEY (id),
    FOREIGN KEY (tournament_id) REFERENCES Tournament(id)
);

CREATE TABLE Player_match
(
    match_id INTEGER NOT NULL,
    player_id INTEGER NOT NULL,
    team_id INTEGER NOT NULL,
    PRIMARY KEY(match_id, player_id),
    FOREIGN KEY(match_id) REFERENCES Matches(id),
    FOREIGN KEY(palyer_id) REFERENCES Player(id),
    
);

CREATE TABLE User_profile
(
    email_address CHAR(80) NOT NULL,
    username CHAR(80),
    superuser boolean,
    password CHAR(128), /*Kommer an på hva slags krypteringsmetode vi bruker, dette er for SHA2 (512?)*/
    PRIMARY KEY(email_address)
);

# Testdata
INSERT INTO Team (team_id, team_name) VALUES (14, 'Superpusene');
INSERT INTO Player (player_id, username, base_rating, display_rating, team_id) VALUES (null, 'Superpusen', 1200, 1200, 1);
INSERT INTO Player (player_id, username, base_rating, display_rating, team_id) VALUES (null, 'LobNobIda', 1200, 1200, 1);