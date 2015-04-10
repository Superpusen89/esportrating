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

  this.add = function(username, team_id, successCallback, errorCallback) {
    var newPlayer = {username: username, team_id: team_id}
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

  this.get = function(id, successCallback, errorCallback) {
    $http.get(REST.path + 'player/' + id).success(function(result) {
      if (typeof (successCallback) === 'function') {
        successCallback(result);
      }
    }).error(function() {
      if (typeof (errorCallback) === 'function') {
        errorCallback();
      }
    });
  };

/** Team **/
  
    this.getAllTeams = function(successCallback, errorCallback) {
    $http.get(REST.path + 'team').success(function(result) {
      if (typeof (successCallback) === 'function') {
        successCallback(result);
      }
    }).error(function() {
      if (typeof (errorCallback) === 'function') {
        errorCallback();
      }
    });
  };

  this.getTeam = function(team_id, successCallback, errorCallback) {
    $http.get(REST.path + 'team/' + team_id).success(function(result) {
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