app.service('daoTournaments', function ($http, REST) {

    this.getAll = function (successCallback, errorCallback) {
        $http.get(REST.path + 'tournament').success(function (result) {
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
        $http.get(REST.path + 'tournament/' + id).success(function (result) {
            if (typeof (successCallback) === 'function') {
                successCallback(result);
            }
        }).error(function () {
            if (typeof (errorCallback) === 'function') {
                errorCallback();
            }
        });
    };

    this.add = function (tournament_name, time_start, time_end, successCallback, errorCallback) {
        var newPlayer = {time_start: time_start, time_end: time_end, tournament_name: tournament_name};
        $http.post(REST.path + 'tournament', newPlayer).success(function (result) {
            if (typeof (successCallback) === 'function') {
                successCallback(result);
            }
        }).error(function () {
            if (typeof (errorCallback) === 'function') {
                errorCallback();
            }
        });
    };

    this.edit = function (tournament_id, tournament_name, time_start, time_end, successCallback, errorCallback) {
        var newPlayer = {tournament_id: tournament_id, tournament_name: tournament_name, time_start: time_start, time_end: time_end};
        $http.put(REST.path + 'tournament', newPlayer).success(function (result) {
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