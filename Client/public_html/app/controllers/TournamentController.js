app.run(function (editableOptions) {
    editableOptions.theme = 'bs3';
});

app.controller('TournamentController', function ($scope, $routeParams, daoTournaments) {
    $scope.status = "Loading...";

    daoTournaments.get($routeParams.tournamentId, function (tournament) {
        $scope.tournament = tournament;
        $scope.status = "Successfully loaded Tournament " + $routeParams.tournamentId;
    }, function () {
        $scope.status = "Error loading Tournament " + $routeParams.tournamentId;
    });

    /********** FIX YES **********/
    $scope.saveName = function (data) {
        var tournament_id = parseInt($routeParams.tournamentId);
        var tournament_name = data;

        daoTournaments.edit(tournament_id, tournament_name,function () {
//          $scope.tournaments.push({username: username, team_name: team_name});
            $scope.status = "Successfully edited tournament " + tournament_name;
        }, function () {
            $scope.status = "Error editing tournament";
        });
    };

//    $scope.saveStartTime = function (data) {
//        var tournament_id = parseInt($routeParams.tournamentId);
//        var tournament_name = $scope.tournament.data[0].tournament_name;
//        var time_start = data;
//        var time_end = $scope.tournament.data[0].time_end;
//
//        daoTournaments.edit(tournament_id, tournament_name, time_start, time_end, function () {
////          $scope.tournaments.push({username: username, team_name: team_name});
//            $scope.status = "Successfully edited tournament " + tournament_name;
//        }, function () {
//            $scope.status = "Error editing tournament";
//        });
//    };
//
//    $scope.saveEndTime = function (data) {
//        var tournament_id = parseInt($routeParams.tournamentId);
//        var tournament_name = $scope.tournament.data[0].tournament_name;
//        var time_start = $scope.tournament.data[0].time_start;
//        var time_end = data;
//
//        daoTournaments.edit(tournament_id, tournament_name, time_start, time_end, function () {
////          $scope.tournaments.push({username: username, team_name: team_name});
//            $scope.status = "Successfully edited tournament " + tournament_name;
//        }, function () {
//            $scope.status = "Error editing tournament";
//        });
//    };

});

