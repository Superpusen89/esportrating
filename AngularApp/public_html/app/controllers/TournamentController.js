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
    $scope.saveData = function (data) {
        var tournament_name = parseInt($routeParams.playerId);
        var time_start = data;
        var time_end = $scope.player.data[0].team_id;
       
        daoTournaments.edit(tournament_name, time_start, time_end, function () {
//          $scope.tournaments.push({username: username, team_name: team_name});
            $scope.status = "Successfully edited tournament " + tournament_name;
        }, function () {
            $scope.status = "Error editing tournament";
        });
    };

});

