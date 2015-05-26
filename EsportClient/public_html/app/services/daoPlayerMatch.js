/* 
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

app.service('daoPlayerMatch', function ($http, REST) {

    this.add = function (match_id, player_id, team_id, successCallback, errorCallback) {
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

    this.get = function (match_id, team_id, successCallback, errorCallback) {
        $http.get(REST.path + 'player_match/' + match_id + ',' + team_id).success(function (result) {
            if (typeof (successCallback) === 'function') {
                successCallback(result);
            }
        }).error(function () {
            if (typeof (errorCallback) === 'function') {
                errorCallback();
            }
        });
    };


    this.edit = function (match_id, old_team_id, new_team_id, old_player_id, new_player_id, successCallback, errorCallback) {
        var newPlayerMatch = {match_id: match_id, old_team_id: old_team_id, new_team_id: new_team_id, old_player_id: old_player_id, new_player_id: new_player_id};
        $http.put(REST.path + 'player_match', newPlayerMatch).success(function (result) {
            if (typeof (successCallback) === 'function') {
                successCallback(result);
            }
        }).error(function () {
            if (typeof (errorCallback) === 'function') {
                errorCallback();
            }
        });
    };

    this.delete = function (match_id, successCallback, errorCallback) {
        console.log("DETETE " + match_id);
        var newPlayerMatch = {match_id: match_id};
        $http.put(REST.path + 'delete_player_match', newPlayerMatch).success(function (result) {
            if (typeof (successCallback) === 'function') {
                successCallback(result);
            }
        }).error(function () {
            if (typeof (errorCallback) === 'function') {
                errorCallback();
            }
        });
    };

    this.calculate = function (match_id, successCallback, errorCallback) {
        console.log("CALCULATE " + match_id);
        var matchId = {match_id: match_id};
        $http.put(REST.path + 'calculate', matchId).success(function (result) {
            if (typeof (successCallback) === 'function') {
                successCallback(result);
            }
        }).error(function () {
            if (typeof (errorCallback) === 'function') {
                errorCallback();
            }
        });
    };

    this.reset = function (match_id, successCallback, errorCallback) {
        console.log("resetELO " + match_id);
        var matchId = {match_id: match_id};
        $http.put(REST.path + 'resetELO', matchId).success(function (result) {
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