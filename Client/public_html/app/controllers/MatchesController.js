app.controller('MatchesController', function ($scope, daoMatches) {
    $scope.status = "...loading";

//    jQuery(document).ready(function ($) {
//        $(".clickable-row").click(function () {
//            window.document.location = $(this).data("href");
//        });
//    });

    console.log('matchescontroller loaded');

    daoMatches.getAll(function (matches) {
        $scope.matches = matches.data;
        $scope.status = "Successfully loaded matches";
    }, function () {
        $scope.status = "Error loading matches";
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

    $scope.spoilers = function () {

        console.log("clicked");
        elements = document.getElementsByName("hidden");
        spans = document.getElementsByName("spoilerspan");
        for (var i = 0; i < elements.length; i++) {
            elements[i].style.display = "block";
            spans[i].style.display = "none";
        }
    };

    $scope.showRow = function (index) {
        console.log("ROW clicked");
        document.getElementById("row"+index).style.display = "block";
        document.getElementById("hide"+index).style.display = "none";
    };

});

