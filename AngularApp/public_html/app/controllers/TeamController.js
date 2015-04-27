app.controller('TeamController', function ($scope, $routeParams, daoTeams) {
    $scope.status = "Loading...";

    daoTeams.getTeam($routeParams.teamId, function (team) {
        $scope.team = team;
        $scope.status = "Successfully loaded team " + $routeParams.teamId;
    }, function () {
        $scope.status = "Error loading team " + $routeParams.teamId;
    });

    $scope.saveData = function (data) {
        var team_id = parseInt($routeParams.teamId);
        var team_name = data;
        daoTeams.edit(team_id, team_name, function () {
//            $scope.players.push({username: username, team_name: team_name});
            $scope.status = "Successfully edited team " + team_id;
        }, function () {
            $scope.status = "Error editing team";
        });
    };

});

