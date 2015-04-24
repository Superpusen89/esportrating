app.controller('MatchesController', function ($scope, daoMatches) {
    $scope.status = "";

    daoMatches.getAll(function (matches) {
        $scope.matches = matches.data;
        $scope.status = "";
    }, function () {
        $scope.status = "Error loading matches";
    });

    $scope.addMatch = function () {
        var time_start = $scope.newMatch.time_start;
        var time_end = $scope.newMatch.time_end;
        var winning_team_id = $scope.newMatch.winning_team_id;
        var losing_team_id = $scope.newMatch.losing_team_id;
        var tournament_id = $scope.newMatch.tournament_id;

        daoMatches.addMatch(time_start, time_end, winning_team_id, losing_team_id, tournament_id, function () {
            $scope.matches.push({time_start: time_start, time_end: time_end, winning_team_id: winning_team_id, losing_team_id: losing_team_id, tournament_id: tournament_id});
            $scope.status = "Successfully created new match ";
        }, function () {
            $scope.status = "Error creating new match";
        });
        $scope.newMatch.time_start = '';
        $scope.newMatch.time_end = '';
        $scope.newMatch.winning_team_id = '';
        $scope.newMatch.losing_team_id = '';
        $scope.newMatch.tournament_id = '';
    };


});