app.controller('PlayersController', function ($scope, daoPlayers) {
    $scope.status = "Loading...";
    $scope.statusTeams = "Loading...";

    daoPlayers.getAll(function (players) {
        $scope.players = players.data;

        for (i = 0; i < $scope.players.length; i++) {
            if ($scope.players[i].team_name === 'null') {
                $scope.players[i].team_name = '';
            }
        }

        $scope.status = "";
    }, function () {
        $scope.status = "Error loading Players";
    });
    
    /*
     * Code taken from 
     * http://jsfiddle.net/gweur/
     * http://stackoverflow.com/questions/18789973/sortable-table-columns-with-angularjs
     */
        $scope.sort = {
            column: '',
            descending: false
        };    
        $scope.changeSorting = function(column) {

            var sort = $scope.sort;
 
            if (sort.column == column) {
                sort.descending = !sort.descending;
            } else {
                sort.column = column;
                sort.descending = false;
            }
        };
    /*
     * code end
     */
});