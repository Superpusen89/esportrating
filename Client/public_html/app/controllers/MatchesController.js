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


});

