app.controller('AddTeamController', function ($scope, daoTeams) {
    $scope.status = "";

    $scope.addTeam = function () {
        var team_name = $scope.newTeam.team_name;

        daoTeams.add(team_name, function (team) {
//            $scope.team = team;
//            console.log('The team id is ' + $scope.team);
//            $scope.teams.push({team_name: team_name, id: $scope.team});
            $scope.status = "Successfully created new team " + team_name;
        }, function () {
            $scope.status = "Error creating new team.";
        });
        $scope.newTeam.team_name = '';
    };

});