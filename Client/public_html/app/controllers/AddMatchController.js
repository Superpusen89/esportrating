app.controller('AddMatchController', function ($scope, daoMatches, daoPlayers, daoTeams, daoTournaments, daoPlayerMatch) {
    $scope.status = "";

    $scope.addMatch = function () {
        var match_time_start = $scope.newMatch.match_time_start;
        var match_time_end = $scope.newMatch.match_time_end;
        var team_1_id = $scope.newMatch.team_1_id;
        var team_2_id = $scope.newMatch.team_2_id;
        var winning_team_id = -1;
        var losing_team_id = -1;

        if ($scope.entities[0].checked === true) {
            winning_team_id = $scope.newMatch.team_1_id;
            losing_team_id = $scope.newMatch.team_2_id;
        }
        ;
        if ($scope.entities[1].checked === true) {
            winning_team_id = $scope.newMatch.team_2_id;
            losing_team_id = $scope.newMatch.team_1_id;
        }
        ;

        var tournament_id = $scope.newMatch.tournament_id;

        console.log('The match time is ' + match_time_start);
 
        daoMatches.add(match_time_start, match_time_end, team_1_id, team_2_id, winning_team_id, losing_team_id, tournament_id, function (match) {
            $scope.match = match;
            console.log('The match id is ' + $scope.match);
            console.log($scope.entities[0].checked);
//            $scope.matches.push({id: $scope.match, match_time_start: match_time_start, match_time_end: match_time_end, team_1_id: team_1_id, team_2_id: team_2_id, winning_team_id: winning_team_id, losing_team_id: losing_team_id, tournament_id: tournament_id});

            var checkedBoxes = getCheckedBoxes("pcheckbox");
            for (i = 0; i < checkedBoxes.length; i++) {
                console.log('!!!!!!!!!' + $scope.match + ' ' + checkedBoxes[i].value + ' ' + team_1_id);

                var match_id = parseInt($scope.match);
                var player_id = parseInt(checkedBoxes[i].value);
                daoPlayerMatch.addPlayerMatch(match_id, player_id, team_1_id, function () {
                    $scope.status = "Successfully created new player_match ";
                }, function () {
                    $scope.status = "Error creating new player_match";
                });

                $scope.checked1 = 0;
            }

            var checkedBoxes2 = getCheckedBoxes("pcheckbox2");
            for (i = 0; i < checkedBoxes2.length; i++) {
                console.log('!!!!!!!!!' + $scope.match + ' ' + checkedBoxes2[i].value + ' ' + team_2_id);

                var match_id2 = parseInt($scope.match);
                var player_id2 = parseInt(checkedBoxes2[i].value);
                daoPlayerMatch.addPlayerMatch(match_id2, player_id2, team_2_id, function () {
                    $scope.status = "Successfully created new player_match ";
                }, function () {
                    $scope.status = "Error creating new player_match";
                });

                $scope.checked2 = 0;
            }

//            $scope.match, checkedBoxes[i].value, team_1_id


            $scope.status = "Successfully created new match ";
        }, function () {
            $scope.status = "Error creating new match";
        });

        $scope.newMatch.match_time_start = '';
        $scope.newMatch.match_time_end = '';
        $scope.newMatch.team_1_id = '';
        $scope.newMatch.team_2_id = '';
        $scope.newMatch.tournament_id = '';
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
            if (model === $scope.players[i].id) {
                return $scope.players[i].id + ' ' + $scope.players[i].username;
            }
        }
    };

    $scope.entities = [{
            checked: false
        }, {
            checked: false
        }
    ]

    $scope.updateSelection = function (position, entities) {
        angular.forEach(entities, function (subscription, index) {
            if (position != index)
                subscription.checked = false;
        });
    }

    $scope.onSelect1 = function ($model) {
        console.log('please ' + $model);
        team1 = $model;

        daoPlayers.getTeamPlayers(team1, function (players) {
            $scope.players1 = players.data;
            console.log('********************** scope players data' + $scope.players1.username);
            console.log('********************** scope teamplayers' + team1);
        }, function () {
            console.log('Error loading teamplayers');
        });
    };

    $scope.onSelect2 = function ($model) {
        console.log('please ' + $model);
        team2 = $model;

        daoPlayers.getTeamPlayers(team2, function (players) {
            $scope.players2 = players.data;
            console.log('********************** scope team2players' + team2);
        }, function () {
            console.log('Error loading team2players');
        });
    };

    $scope.onSelect3 = function ($model) {
        console.log('please the id is ' + $model);
        player1 = $model;
        daoPlayers.get(player1, function (player) {
            $scope.players1.push(player.data[0]);
            console.log('----------' + player.data[0].id + ' ' + player.data[0].username);
        });
    };

    $scope.onSelect4 = function ($model) {
        console.log('please ' + $model);
        player2 = $model;
        daoPlayers.get(player2, function (player) {
            $scope.players2.push(player.data[0]);
            console.log('----------' + player.data[0].id);
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
            }
        }
        // Return the array if it is non-empty, or null
        return checkboxesChecked.length > 0 ? checkboxesChecked : null;
    }
});