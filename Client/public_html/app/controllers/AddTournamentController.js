app.controller('AddTournamentController', function ($scope, daoTournaments) {
    $scope.status = "";


    $scope.addTournament = function () {

        $scope.status = "";

        var tournament_name = $scope.newTournament.tournament_name;

        daoTournaments.add(tournament_name, function () {
            $scope.status = "Successfully created new tournament " + tournament_name;
        }, function () {
            $scope.status = "Error creating new tournament " + tournament_name;
        });
        $scope.newTournament.tournament_name = '';
    };
});