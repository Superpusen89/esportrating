app.controller('TournamentsController', function ($scope, daoTournaments) {
    $scope.status = "Loading...";

    daoTournaments.getAll(function (tournaments) {
        $scope.tournaments = tournaments.data;
        $scope.status = "Successfully loaded Tournaments";
    }, function () {
        $scope.status = "Error loading Tournaments";
    });
});