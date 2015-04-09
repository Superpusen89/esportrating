app.controller('PlayerController', function($scope, $routeParams, daoPlayers) {
  $scope.status = "Loading...";

  daoPlayers.get($routeParams.playerId, function(player) {
    $scope.player = player;
    $scope.status = "Successfully loaded Player " + $routeParams.playerId;
  }, function() {
    $scope.status = "Error loading Player " + $routeParams.playerId;
  });
  
      daoPlayers.getAllTeams(function (teams) {
        $scope.teams = teams.data;
        $scope.statusTeams = "Successfully loaded Teams";
    }, function () {
        $scope.statusTeams = "Error loading Teams";
    }); 
  
});

