app.service('daoPlayers', function ($http, REST) {

    this.getAll = function (successCallback, errorCallback) {
        $http.get(REST.path + 'getplayers').success(function (result) {
            if (typeof (successCallback) === 'function') {
                successCallback(result);
            }
        }).error(function () {
            if (typeof (errorCallback) === 'function') {
                errorCallback();
            }
        });
    };

    this.get = function (id, successCallback, errorCallback) {
        $http.get(REST.path + 'player/' + id).success(function (result) {
            if (typeof (successCallback) === 'function') {
                successCallback(result);
            }
        }).error(function () {
            if (typeof (errorCallback) === 'function') {
                errorCallback();
            }
        });
    };

    this.getTeamPlayers = function (id, successCallback, errorCallback) {
        $http.get(REST.path + 'team_player/' + id).success(function (result) {
            if (typeof (successCallback) === 'function') {
                successCallback(result);
            }
        }).error(function () {
            if (typeof (errorCallback) === 'function') {
                errorCallback();
            }
        });
    };

    this.add = function (username, team_id, successCallback, errorCallback) {
        var newPlayer = {username: username, team_id: team_id};
        $http.post(REST.path + 'player', newPlayer).success(function (result) {
            if (typeof (successCallback) === 'function') {
                successCallback(result);
            }
        }).error(function () {
            if (typeof (errorCallback) === 'function') {
                errorCallback();
            }
        });
    };

    this.edit = function (player_id, username, team_id, base_rating, display_rating, successCallback, errorCallback) {
        var newPlayer = {player_id: player_id, username: username, team_id: team_id, base_rating: base_rating, display_rating: display_rating};
        $http.put(REST.path + 'player', newPlayer).success(function (result) {
            if (typeof (successCallback) === 'function') {
                successCallback(result);
            }
        }).error(function () {
            if (typeof (errorCallback) === 'function') {
                errorCallback();
            }
        });
    };

});