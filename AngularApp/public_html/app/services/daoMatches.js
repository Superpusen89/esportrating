app.service('daoMatches', function ($http, REST) {

    this.getAll = function (successCallback, errorCallback) {
        $http.get(REST.path + 'match').success(function (result) {
            if (typeof (successCallback) === 'function') {
                successCallback(result);
            }
        }).error(function () {
            if (typeof (errorCallback) === 'function') {
                errorCallback();
            }
        });
    };

    this.addMatch = function (time_start, time_end, winning_team_id, losing_team_id, tournament_id, successCallback, errorCallback) {
        var newMatch = {match_time_start: time_start, match_time_end: time_end, winning_team_id: winning_team_id, losing_team_id: losing_team_id, tournament_id: tournament_id};
        $http.post(REST.path + 'match', newMatch).success(function (result) {
            if (typeof (successCallback) === 'function') {
                successCallback(result);
            }
        }).error(function () {
            if (typeof (errorCallback) === 'function') {
                errorCallback();
            }
        });
    };

    this.edit = function (time_start, time_end, winning_team_id, losing_team_id, tournament_id, successCallback, errorCallback) {
        var newMatch = {time_start: time_start, time_end: time_end, winning_team_id: winning_team_id, losing_team_id: losing_team_id, tournament_id: tournament_id};
        $http.put(REST.path + 'match', newMatch).success(function (result) {
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