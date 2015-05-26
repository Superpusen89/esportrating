app.run(function (editableOptions) {
    editableOptions.theme = 'bs2';
});

app.controller('MatchController', function ($scope, $routeParams, daoMatches, daoPlayerMatch, daoTeams, daoPlayers, daoTournaments) {
    $scope.status = "Loading match ...";

    daoMatches.get($routeParams.matchId, function (match) {
        $scope.match = match;
        /*************************** GET PLAYER_MATC FOR TEAM 1 ***********************************************/
        daoPlayerMatch.get($routeParams.matchId, $scope.match.data[0].team_1_id, function (playermatch) {
            $scope.players1 = playermatch.data;
            $scope.status = "";
        }, function () {
            $scope.status = "Error loading winning team.";
        });
        /*************************** GET PLAYER_MATC FOR TEAM 2 ***********************************************/
        daoPlayerMatch.get($routeParams.matchId, $scope.match.data[0].team_2_id, function (playermatch) {
            $scope.players2 = playermatch.data;
            $scope.status = "";
        }, function () {
            $scope.status = "Error loading losing team.";
        });
        
        /**** The following code has been taken from somewhere **/
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
        /*************** code end *******************/

        /*************************** SET INPUT FIELD VALUES ***********************************************/
        if (document.getElementById("team_1") !== null) {
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
        }

        var startDate = new Date($scope.match.data[0].f_time_start);
        var currentDate = new Date();
        var form = document.getElementById("editMatch");

        /*
         * Code taken from 
         * http://stackoverflow.com/questions/7709803/javascript-get-minutes-between-two-dates
         */
        var start = new Date($scope.match.data[0].match_time_start);
        var end = new Date($scope.match.data[0].match_time_end);
        var diffMs = (end - start); //milliseconds
//        var diffDays = Math.round(diffMs / 86400000); // days
//        var diffHrs = Math.round((diffMs % 86400000) / 3600000); // hours
        var diffMins = Math.round(((diffMs % 86400000) % 3600000) / 60000); // minutes
        $scope.duration = diffMins;
        console.log("start " + start + " end " + end + " diffms " + diffMs + " diffmins " + diffMins)

        /*
         * end code
         */

        if (startDate.getMonth() !== currentDate.getMonth() || startDate.getYear() !== currentDate.getYear()) {
            var elements = form.elements;
            for (var i = 0, len = elements.length; i < len; ++i) {
                elements[i].readOnly = true;
            }
            document.getElementById("submit").disabled = true;
            document.getElementById("error").innerHTML = "<br><br>This match is too old to be edited.";
        } else {
            console.log("startmonth " + startDate.getMonth() + " curmonth " + currentDate.getMonth() + " startyear " + startDate.getYear() + " curyear" + currentDate.getYear());
        }

    }, function () {
        $scope.status = "Error loading match.";
    });




    /*************************** ON PRESS SAVE ***********************************************/
    $scope.editMatch = function () {

        var match_time_start = $scope.newMatch.match_time_start;
        console.log(match_time_start);
        var match_time_end = $scope.newMatch.match_time_end;
        var team_1_id = parseInt($scope.newMatch.team_1_id);
        var team_2_id = parseInt($scope.newMatch.team_2_id);
        var winning_team_id = parseInt($scope.newMatch.winning_team_id);
        var losing_team_id = parseInt($scope.newMatch.losing_team_id);
        var tournament_id = parseInt($scope.newMatch.tournament_id);
        var match_id = parseInt($routeParams.matchId);
        /****************************** FIND WINNING TEAM ***************************************/
        if ($scope.entities[0].checked === true) {
            winning_team_id = $scope.newMatch.team_1_id;
            losing_team_id = $scope.newMatch.team_2_id;
        }

        if ($scope.entities[1].checked === true) {
            winning_team_id = $scope.newMatch.team_2_id;
            losing_team_id = $scope.newMatch.team_1_id;
        }

        /*********************************************************** VALIDATE ***************************************************/
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

        /*
         * code end
         */

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

            /******************** DELETE PLAYER MATCH *************************************/
            daoPlayerMatch.reset(match_id, function () {
                console.log("Success resetting Player_match");
            }, function () {
                console.log("Error resetting Player_match");
            });

            daoPlayerMatch.delete(match_id, function () {
                console.log("Success deleting Player_match");
            }, function () {
                console.log("Error deleting Player_match");
            });
            /****************************** EDIT MATCH ********************************************************************/
            daoMatches.edit(match_id, match_time_start, match_time_end, team_1_id, team_2_id, winning_team_id, losing_team_id, tournament_id, function (match) {
                $scope.match = match;
                var checkedBoxes = getCheckedBoxes("pcheckbox");
                for (i = 0; i < checkedBoxes.length; i++) {
                    var new_team_id = parseInt($scope.newMatch.team_1_id);
                    var new_player_id = parseInt(checkedBoxes[i].value);
                    /****************************** ADD TO PLAYER MATCH ******************************************************/

                    console.log("***----**** " + match_id + " new_player_id " + new_player_id + " new_team_id " + new_team_id);
                    daoPlayerMatch.add(match_id, new_player_id, new_team_id, function () {
                        $scope.status = "Successfully edited match.";
                    }, function () {
                        $scope.status = "Error editing match.";
                    });
                    // $scope.checked1 = 0;
                }

                var checkedBoxes2 = getCheckedBoxes("pcheckbox2");
                for (i = 0; i < checkedBoxes2.length; i++) {
                    var new_team_id_2 = parseInt($scope.newMatch.team_2_id);
                    var new_player_id_2 = parseInt(checkedBoxes2[i].value);
                    console.log("***----**** " + match_id + " new_player_id " + new_player_id_2 + " new_team_id " + new_team_id_2);
                    daoPlayerMatch.add(match_id, new_player_id_2, new_team_id_2, function () {
                        $scope.status = "Successfully edited match. ";
                    }, function () {
                        $scope.status = "Error editing match.";
                    });
                    $scope.checked2 = 0;
                }

                $scope.status = "Successfully created new match";

                daoPlayerMatch.calculate(match_id, function () {
                    console.log("Successfully calculated ELO-rating ");
                }, function () {
                    console.log("ELO-calculation failed");
                });
            }, function () {
                $scope.status = "Error creating new match";
            });
        }
    }
    ;
    daoPlayers.getAll(function (players) {
        $scope.players = players.data;
        $scope.status = "";
    }, function () {
        $scope.status = "Error loading players.";
    });
    daoTeams.getAll(function (teams) {
        $scope.teams = teams.data;
    }, function () {
        console.log('Error loading teams');
    });
    daoTournaments.getAll(function (tournaments) {
        $scope.tournaments = tournaments.data;
    }, function () {
        console.log('Error loading tournaments');
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

    /*
     * 
     * following code taken from 
     * http://stackoverflow.com/questions/15207788/calling-a-function-when-ng-repeat-has-finished
     * and
     * http://www.w3schools.com/jsref/met_doc_getelementsbyname.asp
     */

//    $scope.$on('ngRepeatFinished', function (ngRepeatFinishedEvent) {
//        console.log("CHECK CHECKBOXES");
//        var x = document.getElementsByName("pcheckbox");
//        for (i = 0; i < x.length; i++) {
//            if (x[i].type == "checkbox") {
//                x[i].checked = true;
//                console.log(i);
//                console.log("CHECBOX LENGTH VALUE IS ") + x[i];
//            }
//        }
//
//
//        console.log("CHECK CHECKBOXES 2");
//        var y = document.getElementsByName("pcheckbox2");
//        for (i = 0; i < y.length; i++) {
//            if (y[i].type == "checkbox") {
//                y[i].checked = true;
//
//                console.log("CHECBOX LENGTH VALUE IS ") + y[i].value;
//            }
//        }
//    });

    /*
     * code end
     */

    /* Following code is taken from Stackoverflow*/


//    $scope.limit = 5;
//    $scope.items1 = [];
//    $scope.checked1 = 0;
//    for (var i = 0; i < 100; i++) {
//        $scope.items1.push({team1: false})
//    }
//
//    $scope.checkChanged1 = function (item1) {
//        if (item1.team1)
//            $scope.checked1++;
//        else
//            $scope.checked1--;
//    }
//
//    $scope.items2 = [];
//    $scope.checked2 = 0;
//    for (var i = 0; i < 100; i++) {
//        $scope.items2.push({team2: false})
//    }
//
//    $scope.checkChanged2 = function (item2) {
//        if (item2.team2)
//            $scope.checked2++;
//        else
//            $scope.checked2--;
//    }
//
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

