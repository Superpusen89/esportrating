app.controller('TeamsController', function ($scope, daoTeams) {
    $scope.status = "";

    daoTeams.getAll(function (teams) {
        $scope.teams = teams.data;
        $scope.statusTeams = "";
        console.log('**********************' + $scope.teams);
    }, function () {
        $scope.statusTeams = "Error loading Teams";
    });

});