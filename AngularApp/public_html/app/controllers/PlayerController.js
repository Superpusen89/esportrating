app.run(function (editableOptions) {
    editableOptions.theme = 'bs3';
});

app.controller('PlayerController', function ($scope, $routeParams, daoPlayers) {
    $scope.status = "Loading...";

    daoPlayers.get($routeParams.playerId, function (player) {
        $scope.player = player;
        $scope.status = "Successfully loaded Player " + $routeParams.playerId;
    }, function () {
        $scope.status = "Error loading Player " + $routeParams.playerId;
    });

    daoPlayers.getAllTeams(function (teams) {
        $scope.teams = teams.data;
        $scope.statusTeams = "Successfully loaded Teams";
    }, function () {
        $scope.statusTeams = "Error loading Teams";
    });

    $scope.validateInput = function (data) {

        var teams = $scope.teams.length;
        var teamarray = [];
        for (i = 0; i < teams; i++) {
            teamarray.push($scope.teams[i].team_name);
        }

        if ($.inArray(data, teamarray) !== -1) {
            console.log('1. Data in the array: ' + data);
            daoPlayers.getTeamId(data, function (data) {
                $scope.team_id = data;
                console.log('2. Data sent to scope.team_id: ' + data);
                console.log('3. scope.team_id received : ' + data);
            });
            
            console.log('4. scope.team_id outside of function : ' + $scope.team_id);
            var player_id = parseInt($routeParams.playerId);
            var username = $scope.player.data[0].username;
            var team_id = $scope.team_id.data[0].id;
            var base_rating = $scope.player.data[0].base_rating;
            var display_rating = $scope.player.data[0].display_rating;

            console.log(player_id + ' ' + username + ' Team id: ' + team_id + ' Ratings: ' + base_rating + '' + display_rating)
            
            daoPlayers.edit(player_id, username, team_id, base_rating, display_rating, function () {
//            $scope.players.push({username: username, team_name: team_name});
                $scope.status = "Successfully edited team " + username;
            }, function () {
                $scope.status = "Error editing team";
            });
        } else {
            return "Team does not exist ";
        }
    };

    $scope.saveData = function (data) {
        var player_id = parseInt($routeParams.playerId);
        var username = data;
        var team_id = $scope.player.data[0].team_id;
        var base_rating = $scope.player.data[0].base_rating;
        var display_rating = $scope.player.data[0].display_rating;
        daoPlayers.edit(player_id, username, team_id, base_rating, display_rating, function () {
//            $scope.players.push({username: username, team_name: team_name});
            $scope.status = "Successfully edited player " + username;
        }, function () {
            $scope.status = "Error editing player";
        });
    };

});

