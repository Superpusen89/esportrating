app.controller('TournamentsController', function ($scope, daoTournaments) {
    $scope.status = "Loading tournaments ...";

    daoTournaments.getAll(function (tournaments) {
        $scope.tournaments = tournaments.data;
        $scope.status = "";
    }, function () {
        $scope.status = "Error loading tournaments";
    });
});