app.controller('PlayersController', function ($scope, daoPlayers) {
    $scope.status = "Loading...";
    $scope.statusTeams = "Loading...";

    daoPlayers.getAll(function (players) {
        $scope.players = players.data;
        $scope.status = "";
    }, function () {
        $scope.status = "Error loading Players";
    });

    $scope.addPlayer = function () {
        var username = $scope.newPlayer.username;
        var team_id = $scope.newPlayer.team_id;
//
//        daoPlayers.getTeam(team_id, function (team) {
//                $scope.team_name = team;
//        });
//
//        var team_name = $scope.team_name.data[0].team_name;

        daoPlayers.add(username, team_id, function () {
            $scope.players.push({username: username, team_id: team_id});
            $scope.players.push({username: username});
            $scope.status = "Successfully created new Player " + username;
        }, function () {
            $scope.status = "Error creating new Player";
        });
        $scope.newPlayer.username = '';
        $scope.newPlayer.team_id = '';
    };
});