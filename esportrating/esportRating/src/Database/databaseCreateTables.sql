

DROP TABLE User_profile;
DROP TABLE Player_match;
DROP TABLE Player;
DROP TABLE Matches;
DROP TABLE Team;
DROP TABLE Tournament;

CREATE TABLE Team
(
    id INTEGER NOT NULL AUTO_INCREMENT, 
    team_id INTEGER UNIQUE,
    team_name CHAR(80),
    PRIMARY KEY (id)
); /*CHARACTER SET utf8 COLLATE utf8_unicode_ci*/



CREATE TABLE Player
(
    id INTEGER NOT NULL AUTO_INCREMENT,
    player_id INTEGER UNIQUE,
    username CHAR(80),
    base_rating FLOAT,
    display_rating FLOAT,
    team_id INTEGER,
    avatar VARCHAR(200),
    realname CHAR(80),
    countrycode CHAR(5),
    PRIMARY KEY (id),
    FOREIGN KEY (team_id) REFERENCES Team(id)
);

CREATE TABLE Tournament
(
    id INTEGER NOT NULL AUTO_INCREMENT,
    tournament_id INTEGER UNIQUE,
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
    team_1_id INTEGER,
    team_2_id INTEGER,
    winning_team_id INTEGER, 
    losing_team_id INTEGER, 
    match_time_start INT(11),
    match_time_end INT(11),
    PRIMARY KEY (id),
    FOREIGN KEY (tournament_id) REFERENCES Tournament(id)
);

CREATE TABLE Player_match
(
    match_id INTEGER NOT NULL,
    player_id INTEGER NOT NULL,
    team_id INTEGER NOT NULL,
    points FLOAT,
    PRIMARY KEY(match_id, player_id),
    FOREIGN KEY(match_id) REFERENCES Matches(id),
    FOREIGN KEY(player_id) REFERENCES Player(id)    
);

CREATE TABLE User_profile
(
    email_address CHAR(80) NOT NULL,
    username CHAR(80),
    superuser boolean,
    password CHAR(128), /*Kommer an på hva slags krypteringsmetode vi bruker, dette er for SHA2 (512?)*/
    PRIMARY KEY(email_address)
)CHARACTER SET utf8 COLLATE utf8_unicode_ci;

# Testdata
INSERT INTO Team (team_name) VALUES ('Superpusene');
INSERT INTO Team (team_name) VALUES ('Guttah');
INSERT INTO Team (team_name) VALUES ('Unicode');
INSERT INTO Player (player_id, username, base_rating, display_rating, team_id, countrycode) VALUES (null, 'Superpusen', 1200, 1200, 1, 'af');
INSERT INTO Player (player_id, username, base_rating, display_rating, team_id, countrycode) VALUES (null, 'LobNobIda', 1300, 1300, 1, 'au');
INSERT INTO Player (player_id, username, base_rating, display_rating, team_id, countrycode) VALUES (null, 'EirikStrongMan', 1200, 1200, 1, 'ar');
INSERT INTO Player (player_id, username, base_rating, display_rating, team_id, countrycode) VALUES (null, 'TommyTeabag', 1400, 1400, 2, 'bv');
INSERT INTO Player (player_id, username, base_rating, display_rating, team_id, countrycode) VALUES (null, 'Kettelz', 1400, 1400, 2, 'aw');
INSERT INTO Player (player_id, username, base_rating, display_rating, team_id, countrycode) VALUES (null, 'Tedzky', 1400, 1400, 2, 'no');
-- INSERT INTO Player (player_id, username, base_rating, display_rating, team_id) VALUES (null, '여보세요', 1400, 1400, 3);
-- INSERT INTO Player (player_id, username, base_rating, display_rating, team_id) VALUES (null, '有什么需要我帮你的', 1400, 1400, 3);
-- INSERT INTO Player (player_id, username, base_rating, display_rating, team_id) VALUES (null, 'お久しぶりですね', 1400, 1400, 3);
-- INSERT INTO Player (player_id, username, base_rating, display_rating, team_id) VALUES (null, 'Trademark™', 1400, 1400, 3);
-- INSERT INTO Player (player_id, username, base_rating, display_rating, team_id) VALUES (null, ' أهلا صديقي/صديقتي!', 1400, 1400, 3);
-- INSERT INTO Player (player_id, username, base_rating, display_rating, team_id) VALUES (null, 'Øystein', 1400, 1400, 3);
INSERT INTO Player (username, base_rating, display_rating, team_id, countrycode) VALUES ('Gemzi', 1348, 1354, 2, 'aq');
INSERT INTO Tournament (tournament_name) VALUES ('TheFirst');
INSERT INTO Matches (tournament_id, winning_team_id, losing_team_id) VALUES (1, 1, 2); 
INSERT INTO Matches (tournament_id, winning_team_id, losing_team_id) VALUES (1, 1, 2); 
INSERT INTO Matches (tournament_id, winning_team_id, losing_team_id) VALUES (1, 2, 1);
INSERT INTO Player_match (match_id, player_id, team_id) VALUES (1, 1, 1);
INSERT INTO Player_match (match_id, player_id, team_id) VALUES (1, 2, 1);
INSERT INTO Player_match (match_id, player_id, team_id) VALUES (1, 3, 1);
INSERT INTO Player_match (match_id, player_id, team_id) VALUES (1, 4, 2);
INSERT INTO Player_match (match_id, player_id, team_id) VALUES (1, 5, 2);
INSERT INTO Player_match (match_id, player_id, team_id) VALUES (1, 6, 2);
INSERT INTO Player_match (match_id, player_id, team_id) VALUES (2, 1, 1);
INSERT INTO Player_match (match_id, player_id, team_id) VALUES (2, 2, 1);
INSERT INTO Player_match (match_id, player_id, team_id) VALUES (2, 3, 1);
INSERT INTO Player_match (match_id, player_id, team_id) VALUES (2, 4, 2);
INSERT INTO Player_match (match_id, player_id, team_id) VALUES (2, 5, 2);
INSERT INTO Player_match (match_id, player_id, team_id) VALUES (2, 6, 2);
INSERT INTO Player_match (match_id, player_id, team_id) VALUES (3, 1, 1);
INSERT INTO Player_match (match_id, player_id, team_id) VALUES (3, 2, 1);
INSERT INTO Player_match (match_id, player_id, team_id) VALUES (3, 3, 1);
INSERT INTO Player_match (match_id, player_id, team_id) VALUES (3, 4, 2);
INSERT INTO Player_match (match_id, player_id, team_id) VALUES (3, 5, 2);
INSERT INTO Player_match (match_id, player_id, team_id) VALUES (3, 6, 2);

 

 
 
