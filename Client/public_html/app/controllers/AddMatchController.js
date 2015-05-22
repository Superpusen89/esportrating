app.controller('AddMatchController', function ($scope, daoMatches, daoPlayers, daoTeams, daoTournaments, daoPlayerMatch) {
    $scope.status = "";
    $scope.addMatch = function () {
        var match_time_start = $scope.newMatch.match_time_start;
        var match_time_end = $scope.newMatch.match_time_end;
        var team_1_id = $scope.newMatch.team_1_id;
        var team_2_id = $scope.newMatch.team_2_id;
        var winning_team_id = -1;
        var losing_team_id = -1;
        console.log("Match time start: " + match_time_start);
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
        /*
         * code from 
         * http://stackoverflow.com/questions/22979762/jquery-check-if-array-contains-duplicate-string
         */

        var boxOne = getCheckedBoxes("pcheckbox");
        var boxTwo = getCheckedBoxes("pcheckbox2");

        if (getCheckedBoxes("pcheckbox") === null || getCheckedBoxes("pcheckbox2") === null) {
            alert("Please select five players for each team");
        }

        var checkedBoxes = boxOne.concat(boxTwo);
        console.log(checkedBoxes.length)
        var valueArray = [];
        for (var i = 0; i < checkedBoxes.length; i++) {
            valueArray.push(checkedBoxes[i].value);
        }

        var recipientsArray = valueArray.sort();
        var reportRecipientsDuplicate = [];
        for (var i = 0; i < recipientsArray.length - 1; i++) {
            if (recipientsArray[i + 1] === recipientsArray[i]) {
                reportRecipientsDuplicate.push(recipientsArray[i]);
                console.log("array values same: " + recipientsArray[i] + " i is " + i);
            }
            console.log("array values dist: " + recipientsArray[i] + " i is " + i);
        }

        /*
         * code end
         */
        var tournamentArray = [];
        for (i = 0; i < $scope.tournaments.length; i++) {
            tournamentArray.push($scope.tournaments[i].id);
        }

        var tournament = 0;
        if ($.inArray(tournament_id, tournamentArray) !== -1) {
            tournament = 1;
        }

        var teamArray = [];
        for (i = 0; i < $scope.teams.length; i++) {
            teamArray.push($scope.teams[i].id);
        }

        var team1 = 0;
        if ($.inArray(team_1_id, teamArray) !== -1) {
            team1 = 1;
        }

        var team2 = 0;
        if ($.inArray(team_2_id, teamArray) !== -1) {
            team2 = 1;
        }

        var startDate = new Date(match_time_start);
        var endDate = new Date(match_time_end);
        var currentDate = new Date();
        if ($scope.entities[0].checked !== true && $scope.entities[1].checked !== true) {
            console.log("No winning team selected");
            alert("Please check a winning team");
        } else if (tournament === 0) {
            alert("Enter a valid tournament")
        } else if (team1 === 0) {
            alert("Enter a valid team")
        } else if (team2 === 0) {
            alert("Enter a valid team")
        } else if (team_1_id === team_2_id) {
            console.log("Teams must be distinct");
            alert("Please select two different teams")
        } else if (startDate.getMonth() !== currentDate.getMonth() || startDate.getYear() !== currentDate.getYear()) {
            alert("The match must be within the current month and year");
        } else if (startDate.getTime() > endDate.getTime()) {
            alert("End time can't be after start time");
        } else if (getCheckedBoxes("pcheckbox") === null || getCheckedBoxes("pcheckbox2") === null) {
            console.log("Wrong player count");
            alert("Please select five players for each team");
        } else if (getCheckedBoxes("pcheckbox").length !== 5 || getCheckedBoxes("pcheckbox2").length !== 5) {
            alert("Both teams must have exactly five players");
        } else if (reportRecipientsDuplicate.length > 0) {
            alert("You can't select the same player more than once");
        }
        else {
            daoMatches.add(match_time_start, match_time_end, team_1_id, team_2_id, winning_team_id, losing_team_id, tournament_id, function (match) {
                $scope.match = match;
                console.log(' +++++++++++++++++++++++++++ The match id is ' + $scope.match);
                console.log($scope.entities[0].checked);
//            $scope.matches.push({id: $scope.match, match_time_start: match_time_start, match_time_end: match_time_end, team_1_id: team_1_id, team_2_id: team_2_id, winning_team_id: winning_team_id, losing_team_id: losing_team_id, tournament_id: tournament_id});

                var match_id = parseInt($scope.match);

                var checkedBoxes = getCheckedBoxes("pcheckbox");
                for (i = 0; i < checkedBoxes.length; i++) {
                    console.log('!!!!!!!!!' + $scope.match + ' ' + checkedBoxes[i].value + ' ' + team_1_id);
                    var player_id = parseInt(checkedBoxes[i].value);
                    daoPlayerMatch.add(match_id, player_id, team_1_id, function () {
                        $scope.status = "Successfully created new player_match ";
                    }, function () {
                        $scope.status = "Error creating new player_match";
                    });
                    $scope.checked1 = 0;
                }

                var checkedBoxes2 = getCheckedBoxes("pcheckbox2");
                for (i = 0; i < checkedBoxes2.length; i++) {
                    console.log('!!!!!!!!!' + $scope.match + ' ' + checkedBoxes2[i].value + ' ' + team_2_id);
                    var player_id2 = parseInt(checkedBoxes2[i].value);
                    daoPlayerMatch.add(match_id, player_id2, team_2_id, function () {
                        $scope.status = "Successfully created new player_match ";
                    }, function () {
                        $scope.status = "Error creating new player_match";
                    });
                    $scope.checked2 = 0;
                }

                daoPlayerMatch.calculate(match_id, function () {
                    console.log("Successfully calculated ELO-rating ");
                }, function () {
                    console.log("ELO-calculation failed");
                });

//            $scope.match, checkedBoxes[i].value, team_1_id
                $scope.status = "Successfully created new match";
            }, function () {
                $scope.status = "Error creating new match";
            });
            $scope.newMatch.match_time_start = '';
            $scope.newMatch.match_time_end = '';
            $scope.newMatch.team_1_id = '';
            $scope.newMatch.team_2_id = '';
            $scope.newMatch.tournament_id = '';

        }
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
        $scope.checked1 = 0;
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
        $scope.checked2 = 0;
    };
    $scope.onSelect3 = function ($model) {
        player1 = $model;
        daoPlayers.get(player1, function (player) {
            $scope.players1.push(player.data[0]);
            document.getElementById("newplayer1").value = "";
        });
    };
    $scope.onSelect4 = function ($model) {
        player2 = $model;
        daoPlayers.get(player2, function (player) {
            $scope.players2.push(player.data[0]);
            document.getElementById("newplayer2").value = "";
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