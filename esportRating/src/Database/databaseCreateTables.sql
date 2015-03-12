
DROP TABLE Player;
DROP TABLE Team;
DROP TABLE Tournament;
DROP TABLE Matches;
DROP TABLE Player_match;
DROP TABLE User_profile;

CREATE TABLE Team
(
    team_id INTEGER NOT NULL,
    team_name CHAR(80),
    PRIMARY KEY (team_id)
);

CREATE TABLE Player
(
    player_id INTEGER NOT NULL,
    username CHAR(80),
    base_rating INTEGER,
    display_rating INTEGER,
    team_id INTEGER,
    PRIMARY KEY (player_id),
    FOREIGN KEY (team_id) REFERENCES Team(team_id)
);

CREATE TABLE Tournament
(
    tournament_id INTEGER NOT NULL,
    time_start TIMESTAMP,
    time_end TIMESTAMP,
    PRIMARY KEY (tournament_id)
);

CREATE TABLE Matches
(
    match_id INTEGER NOT NULL,
    tournament_id INTEGER,
    radiant_team_id INTEGER NOT NULL,
    dire_team_id INTEGER NOT NULL,
    radient_team_win boolean,
    match_time_start TIMESTAMP,
    match_time_end TIMESTAMP,
    PRIMARY KEY (match_id),
    FOREIGN KEY (tournament_id) REFERENCES Tournament(tournament_id)
);

CREATE TABLE Player_match
(
    match_id INTEGER NOT NULL,
    player_id INTEGER NOT NULL,
    team_id INTEGER NOT NULL,
    PRIMARY KEY(match_id, player_id),
    FOREIGN KEY(match_id) REFERENCES Matches(match_id),
    FOREIGN KEY(player_id) REFERENCES Player(player_id)
);

CREATE TABLE User_profile
(
    email_address CHAR(80) NOT NULL,
    username CHAR(80),
    superuser boolean,
    password CHAR(128), /*Kommer an på hva slags krypteringsmetode vi bruker, dette er for SHA2 (512?)*/
    PRIMARY KEY(email_address)
)

# Testdata
INSERT INTO Team VALUES (14, 'Superpusene');
INSERT INTO Player VALUES (1, 'Superpusen', 1200, 1200, 14);
INSERT INTO Player VALUES (2, 'LobNobIda', 1200, 1200, 14);