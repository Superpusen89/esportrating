app.controller('TeamsController', function ($scope, daoTeams) {
    $scope.status = "Loading teams ...";

    daoTeams.getAll(function (teams) {
        $scope.teams = teams.data;
        $scope.status = "";
    }, function () {
        $scope.status = "Error loading Teams";
    });

});