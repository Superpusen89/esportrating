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
        if ($.inArray(data, $scope.teams) !== -1) {
            window.alert('ok! ');
        } else {
            return "Username should be in list" + data;
        }
    };


});

