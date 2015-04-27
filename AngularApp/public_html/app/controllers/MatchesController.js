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
        var winning_team_id = $scope.newMatch.winning_team_id;
        var losing_team_id = $scope.newMatch.losing_team_id;
        if (typeof winning_team_id === 'undefined') {
            winning_team_id = -1;
        };
        if (typeof losing_team_id === 'undefined') {
            losing_team_id = -1;
        };
        var tournament_id = $scope.newMatch.tournament_id;

        daoMatches.addMatch(match_time_start, match_time_end, team_1_id, team_2_id, winning_team_id, losing_team_id, tournament_id, function (match) {
            $scope.match = match;
            console.log('The match id is ' + $scope.match);
            $scope.matches.push({id: $scope.match, match_time_start: match_time_start, match_time_end: match_time_end, team_1_id: team_1_id, team_2_id: team_2_id, winning_team_id: winning_team_id, losing_team_id: losing_team_id, tournament_id: tournament_id});
            $scope.status = "Successfully created new match ";
        }, function () {
            $scope.status = "Error creating new match";
        });
        $scope.newMatch.time_start = '';
        $scope.newMatch.time_end = '';
        $scope.newMatch.team_1_id = '';
        $scope.newMatch.team_2_id = '';
        $scope.newMatch.winning_team_id = '';
        $scope.newMatch.losing_team_id = '';
        $scope.newMatch.tournament_id = '';
    };

    daoMatches.getAllTeams(function (teams) {
        $scope.teams = teams.data;
        $scope.statusTeams = "";
        console.log('**********************' + $scope.teams);
    }, function () {
        console.log('Error loading Teams');
    });

    $scope.formatLabel = function (model) {
        for (var i = 0; i < $scope.teams.length; i++) {
            if (model === $scope.teams[i].id) {
                return $scope.teams[i].team_name;
            }
        }
    };


});