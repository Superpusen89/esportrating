app.run(function (editableOptions) {
    editableOptions.theme = 'bs3';
});

app.controller('MatchController', function ($scope, $routeParams, daoMatches) {
    $scope.status = "Loading...";

    daoMatches.get($routeParams.matchId, function (match) {
        $scope.match = match;
        $scope.status = "Successfully loaded match " + $routeParams.matchId;
    }, function () {
        $scope.status = "Error loading match " + $routeParams.matchId;
    });
});

