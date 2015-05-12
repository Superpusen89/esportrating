app.controller('TournamentsController', function ($scope, daoTournaments) {
    $scope.status = "Loading...";

    daoTournaments.getAll(function (tournaments) {
        $scope.tournaments = tournaments.data;
        $scope.status = "Successfully loaded Tournaments";
    }, function () {
        $scope.status = "Error loading Tournaments";
    });

    $scope.addTournament = function () {
        var tournament_name = $scope.newTournament.tournament_name;
//        var time_start = $scope.newTournament.time_start;
//        var time_end = $scope.newTournament.time_end;

        daoTournaments.add(tournament_name, function () {
            $scope.tournaments.push({tournament_name: tournament_name});
            $scope.status = "Successfully created new Tournament " + tournament_name;
        }, function () {
            $scope.status = "Error creating new Tournament";
        });
        $scope.newTournament.tournament_name = '';
    };
});