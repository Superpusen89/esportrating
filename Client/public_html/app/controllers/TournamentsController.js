app.controller('TournamentsController', function ($scope, daoTournaments) {
    $scope.status = "Loading tournaments ...";

    daoTournaments.getAll(function (tournaments) {
        $scope.tournaments = tournaments.data;
        $scope.status = "";
    }, function () {
        $scope.status = "Error loading tournaments";
    });

    /* Code taken from 
     * http://jsfiddle.net/gweur/
     * http://stackoverflow.com/questions/18789973/sortable-table-columns-with-angularjs
     */
    $scope.sort = {
        column: '',
        descending: false
    };
    $scope.changeSorting = function (column) {

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