/* 
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

function Hey($scope, $http) {
    $scope.doRequest = function () {
        var username = $scope.user.username;
        $http.get('http://0.0.0.0:5001/player/' + username).
                success(function (data) {
                    $scope.name = data.data;
                });
    };
}


function Ho($scope, $http) {
    $scope.doRequest = function () {
        $http.get('http://0.0.0.0:5001/getplayers').
                success(function (data) {
                    $scope.names = data.data;
                });
    };
}

function formCtrl($scope, $http) {
    $scope.master = {player_id:"", username:"", team_id:""};
    $scope.reset = function() {
        $scope.user = angular.copy($scope.master);
    };
    $scope.reset();
    $scope.doRequest = function () {

        var postObject = new Object();
        postObject.player_id = $scope.user.player_id;
        postObject.username = $scope.user.username;
        postObject.team_id = $scope.user.team_id;

        $http.post('http://0.0.0.0:5001/player', postObject).
                success(function (data) {
                    console.log("HERE *******" + data);
                });
    };
};
