app.controller('MatchesController', function ($scope, daoMatches) {
    $scope.status = "";

    daoMatches.getAll(function (matches) {
        $scope.matches = matches.data;
        $scope.status = "";
    }, function () {
        $scope.status = "Error loading matches";
    });

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

        daoMatches.addMatch(match_time_start, match_time_end, team_1_id, team_2_id, winning_team_id, losing_team_id, tournament_id, function (match) {
            $scope.match = match;
            console.log('The match id is ' + $scope.match);
            console.log($scope.entities[0].checked);
            $scope.matches.push({id: $scope.match, match_time_start: match_time_start, match_time_end: match_time_end, team_1_id: team_1_id, team_2_id: team_2_id, winning_team_id: winning_team_id, losing_team_id: losing_team_id, tournament_id: tournament_id});
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

    daoMatches.getAllTeams(function (teams) {
        $scope.teams = teams.data;
        console.log('********************** scope teams' + $scope.teams);
    }, function () {
        console.log('Error loading Teams');
    });

    daoMatches.getAllTournaments(function (tournaments) {
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



});