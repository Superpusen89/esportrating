/* 
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

app.service('daoPlayerMatch', function ($http, REST) {

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
});