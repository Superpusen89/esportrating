app.run(function (editableOptions) {
    editableOptions.theme = 'bs3';
});

app.controller('MatchController', function ($scope, $routeParams, daoMatches, daoPlayerMatch, daoTeams, daoPlayers, daoTournaments) {
    $scope.status = "Loading match ...";

    daoMatches.get($routeParams.matchId, function (match) {
        $scope.match = match;

        /*************************** GET PLAYER_MATC FOR TEAM 1 ***********************************************/
        daoPlayerMatch.get($routeParams.matchId, $scope.match.data[0].team_1_id, function (playermatch) {
            $scope.players1 = playermatch.data;
            console.log("players1 " + $scope.players1[0].player_id)
            $scope.status = "";
        }, function () {
            $scope.status = "Error loading playermatchwinner";
        });

        /*************************** GET PLAYER_MATC FOR TEAM 1 ***********************************************/
        daoPlayerMatch.get($routeParams.matchId, $scope.match.data[0].team_2_id, function (playermatch) {
            $scope.players2 = playermatch.data;
            $scope.status = "";
        }, function () {
            $scope.status = "Error loading playermatchloser";
        });

        if ($scope.match.data[0].team_1_id === $scope.match.data[0].winning_team_id) {
            $scope.entities = [{
                    checked: true
                }, {
                    checked: false
                }
            ]
            $scope.team_1_name = $scope.match.data[0].winning_team;
            $scope.team_2_name = $scope.match.data[0].losing_team;
        } else {
            $scope.entities = [{
                    checked: false
                }, {
                    checked: true
                }
            ]
            $scope.team_2_name = $scope.match.data[0].winning_team;
            $scope.team_1_name = $scope.match.data[0].losing_team;
        }

        /*************************** SET INPUT FIELD VALUES ***********************************************/
        document.getElementById("team_1").value = $scope.match.data[0].team_1_id + " " + $scope.team_1_name;
        document.getElementById("team_2").value = $scope.match.data[0].team_2_id + " " + $scope.team_2_name;
        document.getElementById("start_time").value = $scope.match.data[0].f_time_start;
        document.getElementById("end_time").value = $scope.match.data[0].f_time_end;
        document.getElementById("tournament").value = $scope.match.data[0].tournament_id + " " + $scope.match.data[0].tournament_name;

        /*************************** GET OLD VALUES  ***********************************************/
        $scope.newMatch.match_time_start = $scope.match.data[0].f_time_start;
        $scope.newMatch.match_time_end = $scope.match.data[0].f_time_end;
        $scope.newMatch.team_1_id = parseInt($scope.match.data[0].team_1_id);
        $scope.newMatch.team_2_id = parseInt($scope.match.data[0].team_2_id);
        $scope.newMatch.winning_team_id = parseInt($scope.match.data[0].winning_team_id);
        $scope.newMatch.losing_team_id = parseInt($scope.match.data[0].losing_team_id);
        $scope.newMatch.tournament_id = parseInt($scope.match.data[0].tournament_id);

        $scope.status = "";
    }, function () {
        $scope.status = "Error loading match " + $routeParams.matchId;
    });

    /*************************** ON PRESS SAVE ***********************************************/
    $scope.editMatch = function () {
        var match_time_start = $scope.newMatch.match_time_start;
        var match_time_end = $scope.newMatch.match_time_end;
        var team_1_id = parseInt($scope.newMatch.team_1_id);
        var team_2_id = parseInt($scope.newMatch.team_2_id);
        var winning_team_id = parseInt($scope.newMatch.winning_team_id);
        var losing_team_id = parseInt($scope.newMatch.losing_team_id);
        var tournament_id = parseInt($scope.newMatch.tournament_id);
        var match_id = parseInt($routeParams.matchId);

        console.log("Match time start: " + match_time_start);
        console.log("Match time end: " + match_time_end);
        console.log("Team 1 id: " + team_1_id);
        console.log("Tead 2 id: " + team_2_id);
        console.log("Winning team id: " + winning_team_id);
        console.log("Losing team id: " + losing_team_id);

        /****************************** FIND WINNING TEAM ***************************************/
        if ($scope.entities[0].checked === true) {
            winning_team_id = $scope.newMatch.team_1_id;
            losing_team_id = $scope.newMatch.team_2_id;
        }

        if ($scope.entities[1].checked === true) {
            winning_team_id = $scope.newMatch.team_2_id;
            losing_team_id = $scope.newMatch.team_1_id;
        }


        /******************** DELETE PLAYER MATCH *************************************/
        daoPlayerMatch.delete(match_id, function () {
            $scope.status = "Success deleting Player_match";
        }, function () {
            $scope.status = "Error deleting Player_match";
        });

        /****************************** EDIT MATCH ********************************************************************/
        daoMatches.edit(match_id, match_time_start, match_time_end, team_1_id, team_2_id, winning_team_id, losing_team_id, tournament_id, function (match) {
            $scope.match = match;
            console.log('The match id is ' + $scope.match);
            console.log($scope.entities[0].checked);

            var checkedBoxes = getCheckedBoxes("pcheckbox");
            for (i = 0; i < checkedBoxes.length; i++) {
                console.log('----------------------------- length ' + checkedBoxes.length);
                console.log('---------------------------- scopematch checkboxesvalue teamid' + checkedBoxes[i].value);

                var new_team_id = parseInt(team_1_id);
                console.log("THE TEAM ID = " + new_team_id);

                var new_player_id = parseInt(checkedBoxes[i].value);
                console.log("NEW PLAYER ID IS " + new_player_id);

                console.log("MATCH ID IS " + match_id);

                /****************************** ADD TO PLAYER MATCH ******************************************************/

                daoPlayerMatch.add(match_id, new_player_id, new_team_id, function () {
                    $scope.status = "Successfully edited player_match ";
                }, function () {
                    $scope.status = "Error editing player_match";
                });

                $scope.checked1 = 0;
            }

            var checkedBoxes2 = getCheckedBoxes("pcheckbox2");
            for (i = 0; i < checkedBoxes2.length; i++) {
                console.log('!!!!!!!!!' + $scope.match + ' ' + checkedBoxes2[i].value + ' ' + team_2_id);


                var new_team_id_2 = parseInt($scope.newMatch.team_2_id);
                var new_player_id_2 = parseInt(checkedBoxes2[i].value);

                daoPlayerMatch.add(match_id, new_player_id_2, new_team_id_2, function () {
                    $scope.status = "Successfully edited player_match ";
                }, function () {
                    $scope.status = "Error editing player_match";
                });

                $scope.checked2 = 0;
            }


            $scope.status = "Successfully created new match";
        }, function () {
            $scope.status = "Error creating new match";
        });
    };

    daoPlayers.getAll(function (players) {
        $scope.players = players.data;
        $scope.status = "";
    }, function () {
        $scope.status = "Error loading Players";
    });

    daoTeams.getAll(function (teams) {
        $scope.teams = teams.data;
        console.log('********************** scope teams' + $scope.teams);
    }, function () {
        console.log('Error loading Teams');
    });

    daoTournaments.getAll(function (tournaments) {
        $scope.tournaments = tournaments.data;
        console.log('********************** scope tournament' + $scope.tournaments);
    }, function () {
        console.log('Error loading Tournaments');
    });

    $scope.formatLabel = function (model) {
        for (var i = 0; i < $scope.teams.length; i++) {
            if (model === $scope.teams[i].id) {
                return $scope.teams[i].id + ' ' + $scope.teams[i].team_name;
            }
        }
    };

    $scope.formatTournamentLabel = function (model) {
        for (var i = 0; i < $scope.tournaments.length; i++) {
            if (model === $scope.tournaments[i].id) {
                return $scope.tournaments[i].id + ' ' + $scope.tournaments[i].tournament_name;
            }
        }
    };

    $scope.formatPlayerLabel = function (model) {
        for (var i = 0; i < $scope.players.length; i++) {
            if (model === $scope.players[i].player_id) {
                return $scope.players[i].player_id + ' ' + $scope.players[i].username;
            }
        }
    };

    $scope.updateSelection = function (position, entities) {
        angular.forEach(entities, function (subscription, index) {
            if (position != index)
                subscription.checked = false;
        });
    }

    $scope.onSelect3 = function ($model) {
        console.log('please the id is ' + $model);
        player1 = $model;
        daoPlayers.get(player1, function (player) {
            $scope.players1.push(player.data[0]);
            document.getElementById("newplayer1").value = "";
            console.log('----------' + player.data[0].player_id + ' ' + player.data[0].username);
        });
    };

    $scope.onSelect4 = function ($model) {
        console.log('please ' + $model);
        player2 = $model;
        daoPlayers.get(player2, function (player) {
            $scope.players2.push(player.data[0]);
            document.getElementById("newplayer2").value = "";
            console.log('----------' + player.data[0].player_id);
        });
    };

    $scope.limit = 5;

    $scope.items1 = [];
    $scope.checked1 = 0;
    for (var i = 0; i < 100; i++) {
        $scope.items1.push({team1: false})
    }

    $scope.checkChanged1 = function (item1) {
        if (item1.team1)
            $scope.checked1++;
        else
            $scope.checked1--;
    }

    $scope.items2 = [];
    $scope.checked2 = 0;
    for (var i = 0; i < 100; i++) {
        $scope.items2.push({team2: false})
    }

    $scope.checkChanged2 = function (item2) {
        if (item2.team2)
            $scope.checked2++;
        else
            $scope.checked2--;
    }

    function getCheckedBoxes(chkboxName) {
        var checkboxes = document.getElementsByName(chkboxName);
        var checkboxesChecked = [];
        // loop over them all
        for (var i = 0; i < checkboxes.length; i++) {
            // And stick the checked ones onto an array...
            if (checkboxes[i].checked) {
                checkboxesChecked.push(checkboxes[i]);
                console.log("box is checked and the value is " + checkboxes[i].value)
            }
            console.log("box is unchecked and the value is " + checkboxes[i].value)
            console.log("the length of the boxes is " + checkboxes.length)
        }
        // Return the array if it is non-empty, or null
        return checkboxesChecked.length > 0 ? checkboxesChecked : null;
    }


});

