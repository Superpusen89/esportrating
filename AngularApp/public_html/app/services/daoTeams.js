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
});