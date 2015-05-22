app.controller('TeamsController', function ($scope, daoTeams) {
    $scope.status = "Loading teams ...";

    daoTeams.getAll(function (teams) {
        $scope.teams = teams.data;
        $scope.status = "";
    }, function () {
        $scope.status = "Error loading Teams";
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