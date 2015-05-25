app.run(function (editableOptions) {
    editableOptions.theme = 'bs3';
});

app.controller('TournamentController', function ($scope, $routeParams, daoTournaments, daoMatches) {
    $scope.status = "Loading tournament ...";
    $scope.matchStatus = "Loading matches ...";

    daoTournaments.get($routeParams.tournamentId, function (tournament) {
        $scope.tournament = tournament;
        $scope.status = "";

        daoMatches.getByTournament($routeParams.tournamentId, function (matches) {
            $scope.matches = matches.data;
            $scope.matchStatus = "";
        }, function () {
            $scope.matchStatus = "Error loading matches.";
        });

    }, function () {
        $scope.status = "Error loading tournament.";
    });

    /********** FIX YES **********/
    $scope.saveName = function (data) {
        var tournament_id = parseInt($routeParams.tournamentId);
        var tournament_name = data;

        daoTournaments.edit(tournament_id, tournament_name, function () {
            $scope.status = "Successfully edited tournament " + $routeParams.tournamentId + " " + tournament_name;
        }, function () {
            $scope.status = "Error editing tournament.";
        });
    };

});

