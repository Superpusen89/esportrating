app.controller('PlayersController', function ($scope, daoPlayers) {
    $scope.status = "Loading...";
    $scope.statusTeams = "Loading...";

    daoPlayers.getAll(function (players) {
        $scope.players = players.data;

        for (i = 0; i < $scope.players.length; i++) {
            if ($scope.players[i].team_name === 'null') {
                $scope.players[i].team_name = '';
            }
        }

        $scope.status = "";
    }, function () {
        $scope.status = "Error loading Players";
    });
    
});