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

    this.get = function (id, successCallback, errorCallback) {
        $http.get(REST.path + 'match/' + id).success(function (result) {
            if (typeof (successCallback) === 'function') {
                successCallback(result);
            }
        }).error(function () {
            if (typeof (errorCallback) === 'function') {
                errorCallback();
            }
        });
    };

    this.getByTournament = function (id, successCallback, errorCallback) {
        $http.get(REST.path + 'match_tournament/' + id).success(function (result) {
            if (typeof (successCallback) === 'function') {
                successCallback(result);
            }
        }).error(function () {
            if (typeof (errorCallback) === 'function') {
                errorCallback();
            }
        });
    };

    this.add = function (match_time_start, match_time_end, team_1_id, team_2_id, winning_team_id, losing_team_id, tournament_id, successCallback, errorCallback) {
        var newMatch = {match_time_start: match_time_start, match_time_end: match_time_end, team_1_id: team_1_id, team_2_id: team_2_id, winning_team_id: winning_team_id, losing_team_id: losing_team_id, tournament_id: tournament_id};
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

    this.edit = function (match_id, match_time_start, match_time_end, team_1_id, team_2_id, winning_team_id, losing_team_id, tournament_id, successCallback, errorCallback) {
        var newMatch = {id: match_id, match_time_start: match_time_start, match_time_end: match_time_end, team_1_id: team_1_id, team_2_id: team_2_id, winning_team_id: winning_team_id, losing_team_id: losing_team_id, tournament_id: tournament_id};
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