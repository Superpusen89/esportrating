/* 
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

function Hey($scope, $http) {
    $scope.doRequest = function () {
        var postObject = new Object();
//        $http({
//            url: 'http://0.0.0.0:5001/player',
//            method: "GET",
//            params: {username: "Aragorn"}
//        });
        postObject.username = "";
        $http.get('http://0.0.0.0:5001/player/Superpusen').
                success(function (data) {
                    $scope.name = data;
                });
    };
}


function Ho($scope, $http) {
    $http.get('http://0.0.0.0:5001/getplayers').
            success(function (data) {
                $scope.names = data.data;
            });
}




function jsonp_example($scope, $http) {
    $scope.doRequest = function () {
        /*    $http.get('http://0.0.0.0:5001/team').
         success(function (data) {
         $scope.names = data.data;
         }); */

        var postObject = new Object();
        postObject.player_id = 19;
        postObject.username = "Anthea";
        postObject.team_id = 14;

        $http.post('http://0.0.0.0:5001/player', postObject).
                success(function (data) {
                    console.log("HERE *******" + data);
                });
    };
}
