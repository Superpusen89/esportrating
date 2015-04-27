app.service('daoTeams', function ($http, REST) {


    this.getAllTeams = function (successCallback, errorCallback) {
        $http.get(REST.path + 'team').success(function (result) {
            if (typeof (successCallback) === 'function') {
                successCallback(result);
            }
        }).error(function () {
            if (typeof (errorCallback) === 'function') {
                errorCallback();
            }
        });
    };

    this.getTeam = function (team_id, successCallback, errorCallback) {
        $http.get(REST.path + 'team/' + team_id).success(function (result) {
            if (typeof (successCallback) === 'function') {
                successCallback(result);
            }
        }).error(function () {
            if (typeof (errorCallback) === 'function') {
                errorCallback();
            }
        });
    };

    this.getTeamId = function (team_name, successCallback, errorCallback) {
        $http.get(REST.path + 'team/' + team_name).success(function (result) {
            if (typeof (successCallback) === 'function') {
                successCallback(result);
            }
        }).error(function () {
            if (typeof (errorCallback) === 'function') {
                errorCallback();
            }
        });
    };

    this.addTeam = function (team_name, successCallback, errorCallback) {
        var newTeam = {team_name: team_name};
        $http.post(REST.path + 'team', newTeam).success(function (result) {
            if (typeof (successCallback) === 'function') {
                successCallback(result);
            }
        }).error(function () {
            if (typeof (errorCallback) === 'function') {
                errorCallback();
            }
        });
    };

    this.edit = function (team_id, team_name, successCallback, errorCallback) {
        var newTeam = {team_id: team_id, team_name: team_name};
        $http.put(REST.path + 'team', newTeam).success(function (result) {
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