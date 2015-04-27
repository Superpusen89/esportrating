app.controller('TeamsController', function ($scope, daoTeams) {
    $scope.status = "";

    daoTeams.getAllTeams(function (teams) {
        $scope.teams = teams.data;
        $scope.statusTeams = "";
        console.log($scope.teams);
    }, function () {
        $scope.statusTeams = "Error loading Teams";
    });

    $scope.addTeam = function () {
        var team_name = $scope.newTeam.team_name;

        daoTeams.addTeam(team_name, function () {
            $scope.teams.push({team_name: team_name});
            $scope.status = "Successfully created new team " + team_name;
        }, function () {
            $scope.status = "Error creating new team";
        });
        $scope.newTeam.team_name = '';
    };

});