app.run(function (editableOptions) {
    editableOptions.theme = 'bs3';
});

app.controller('MatchController', function ($scope, $routeParams, daoMatches) {
    $scope.status = "Loading...";

    daoMatches.get($routeParams.matchIs, function (match) {
        $scope.match = match;
        $scope.status = "Successfully loaded match " + $routeParams.matchId;
    }, function () {
        $scope.status = "Error loading match " + $routeParams.matchId;
    });
});

