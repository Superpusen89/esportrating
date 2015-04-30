app.controller('MatchesController', function ($scope, daoMatches) {
    $scope.status = "...loading";
    
    console.log('matchescontroller loaded');

    daoMatches.getAll(function (matches) {
        $scope.matches = matches.data;
        $scope.status = "Successfully loaded matches";
    }, function () {
        $scope.status = "Error loading matches";
    });
});

