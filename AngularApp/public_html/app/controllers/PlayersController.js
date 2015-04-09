app.controller('PlayersController', function($scope, daoPlayers) {
  $scope.status = "Loading...";
  
  daoPlayers.getAll(function(players) {
    $scope.players = players.data;
    $scope.status = "Successfully loaded Players";
  }, function() {
    $scope.status = "Error loading Players";
  });

  $scope.addPlayer = function() {
    var player_id = $scope.newPlayer.player_id;
    var username = $scope.newPlayer.username;
    var team_id = $scope.newPlayer.team_id;
    daoPlayers.add(player_id, username, team_id, function(result) {
      $scope.players.push({player_id: player_id, username: username, team_id: team_id});
      $scope.status = "Successfully created new Player " + username;
    }, function() {
      $scope.status = "Error creating new Player";
    });
    $scope.newPlayer.player_id = '';
    $scope.newPlayer.username = '';
    $scope.newPlayer.team_id = '';
  };

});