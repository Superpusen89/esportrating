app.controller('TeamController', function ($scope, $routeParams, daoTeams, daoPlayers) {
    $scope.status = "Loading team ...";
    $scope.status = "Loading players ...";

    daoTeams.get($routeParams.teamId, function (team) {
        $scope.team = team;
        $scope.status = "";
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

    daoPlayers.getTeamPlayers($routeParams.teamId, function (players) {
        $scope.players = players.data;

        for (i = 0; i < $scope.players.length; i++) {
            if ($scope.players[i].team_name === 'null') {
                $scope.players[i].team_name = 'no team';
            }
        }

        $scope.statusPlayers = "";
    }, function () {
        $scope.statusPlayers = "Error loading Players";
    });

});

