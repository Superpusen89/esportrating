app.service('daoPlayers', function($http, REST) {
    
  this.getAll = function(successCallback, errorCallback) {
    $http.get(REST.path + 'getplayers').success(function(result) {
      if (typeof (successCallback) === 'function') {
        successCallback(result);
      }
    }).error(function() {
      if (typeof (errorCallback) === 'function') {
        errorCallback();
      }
    });
  };

  this.add = function(player_id, username, team_id, successCallback, errorCallback) {
    var newPlayer = {player_id: player_id, username: username, team_id: team_id}
    $http.post(REST.path + 'player', newPlayer).success(function(result) {
      if (typeof (successCallback) === 'function') {
        successCallback(result);
      }
    }).error(function() {
      if (typeof (errorCallback) === 'function') {
        errorCallback();
      }
    });
  };

  this.get = function(username, successCallback, errorCallback) {
    $http.get(REST.path + 'player/' + username).success(function(result) {
      if (typeof (successCallback) === 'function') {
        successCallback(result);
      }
    }).error(function() {
      if (typeof (errorCallback) === 'function') {
        errorCallback();
      }
    });
  };
});
