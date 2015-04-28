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

    this.addMatch = function (match_time_start, match_time_end, team_1_id, team_2_id, winning_team_id, losing_team_id, tournament_id, successCallback, errorCallback) {
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

    this.addPlayerMatch = function (match_id, player_id, team_id, successCallback, errorCallback) {
        var newPlayerMatch = {match_id: match_id, player_id: player_id, team_id: team_id};
        $http.post(REST.path + 'player_match', newPlayerMatch).success(function (result) {
            if (typeof (successCallback) === 'function') {
                successCallback(result);
            }
        }).error(function () {
            if (typeof (errorCallback) === 'function') {
                errorCallback();
            }
        });
    };

    this.edit = function (match_time_start, match_time_end, team_1_id, team_2_id, winning_team_id, losing_team_id, tournament_id, successCallback, errorCallback) {
        var newMatch = {match_time_start: match_time_start, match_time_end: match_time_end, team_1_id: team_1_id, team_2_id: team_2_id, winning_team_id: winning_team_id, losing_team_id: losing_team_id, tournament_id: tournament_id};
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

    this.getAllTournaments = function (successCallback, errorCallback) {
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

    this.getAllPlayers = function (successCallback, errorCallback) {
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

    this.getPlayer = function (id, successCallback, errorCallback) {
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
});