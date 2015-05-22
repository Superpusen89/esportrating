app.run(function (editableOptions) {
    editableOptions.theme = 'bs3';
});

app.controller('PlayerController', function ($scope, $routeParams, daoPlayers, daoCountries, daoTeams) {
    $scope.status = "Loading...";

    daoPlayers.get($routeParams.playerId, function (player) {
        $scope.player = player;

        for (i = 0; i < $scope.player.data.length; i++) {
            console.log($scope.player.data[i].realname);
            if ($scope.player.data[i].team_name === 'null') {
                $scope.player.data[i].team_name = '';
            }
            if ($scope.player.data[i].realname.localeCompare('null') === 0) {
                $scope.player.data[i].realname = '';
            }
        }



        $scope.status = "Successfully loaded Player " + $routeParams.playerId;
    }, function () {
        $scope.status = "Error loading Player " + $routeParams.playerId;
    });

    daoTeams.getAll(function (teams) {
        $scope.teams = teams.data;
        $scope.statusTeams = "Successfully loaded Teams";
    }, function () {
        $scope.statusTeams = "Error loading Teams";
    });

//formats the input selector
    $scope.formatLabelTeam = function (model) {
        console.log("TeamLabelFormatter " + model);
        for (var i = 0; i < $scope.teams.length; i++) {
            if (parseInt(model) === $scope.teams[i].id) {
                console.log("TeamLabelFormatter inside if" + $scope.teams[i].id);
                return $scope.teams[i].team_name;                
            }
            console.log("TeamLabelFormatter outside if ");
        }
    };

    $scope.saveTeam = function (data) {

        var teams = $scope.teams.length;
        var teamarray = [];
        for (i = 0; i < teams; i++) {
            teamarray.push($scope.teams[i].id);
        }

        if ($.inArray(data, teamarray) !== -1) {
            console.log('1. Data in the array: ' + data);
            daoTeams.getTeamId(data, function (data) {
                $scope.team_id = data;
            });

            console.log('4. scope.team_id outside of function : ' + $scope.team_id);
            var player_id = parseInt($routeParams.playerId);
            var username = $scope.player.data[0].username;
            var team_id = data;
            var avatar = $scope.player.data[0].avatar;
            var realname = $scope.player.data[0].realname;
            var country = $scope.player.data[0].countrycode;

//            console.log(player_id + ' ' + username + ' Team id: ' + team_id + ' Ratings: ' + base_rating + '' + display_rating)

            daoPlayers.edit(player_id, username, team_id, avatar, realname, country, function () {
//            $scope.players.push({username: username, team_name: team_name});
                $scope.status = "Successfully edited team " + username;
            }, function () {
                $scope.status = "Error editing team";
            });
        } else {
            return "Team does not exist ";
        }
    };

    daoCountries.getAll(function (countries) {
        $scope.countries = countries.data;
        console.log('********************** scope countries' + $scope.countries);
    }, function () {
        console.log('Error loading countries');
    });

    $scope.formatLabelCountry = function (model) {
        for (var i = 0; i < $scope.countries.length; i++) {
            if (model === $scope.countries[i].alpha_2) {
                return $scope.countries[i].name;
            }
        }
    };

    $scope.saveCountry = function (data) {

        var countries = $scope.countries.length;

        var countryarray = [];
        for (i = 0; i < countries; i++) {
            countryarray.push($scope.countries[i].alpha_2);
        }

        if ($.inArray(data, countryarray) !== -1) {
//            console.log('4. scope.team_id outside of function : ' + $scope.team_id);
            var player_id = parseInt($routeParams.playerId);
            var username = $scope.player.data[0].username;
            var team_id = $scope.player.data[0].team_id;
            var avatar = $scope.player.data[0].avatar;
            var realname = $scope.player.data[0].realname;
            var country = data;

//            console.log(player_id + ' ' + username + ' Team id: ' + team_id + ' Ratings: ' + base_rating + '' + display_rating)

            daoPlayers.edit(player_id, username, team_id, avatar, realname, country, function () {
//            $scope.players.push({username: username, team_name: team_name});
                $scope.status = "Successfully edited team " + username;
            }, function () {
                $scope.status = "Error editing team";
            });
        } else {
            return "Country does not exist ";
        }
    };

    $scope.saveUsername = function (data) {
        console.log("Saving username: " + data);
        var player_id = parseInt($routeParams.playerId);
        var username = data;
        var team_id = $scope.player.data[0].team_id;
        var avatar = $scope.player.data[0].avatar;
        var realname = $scope.player.data[0].realname;
        var country = $scope.player.data[0].countrycode;
        daoPlayers.edit(player_id, username, team_id, avatar, realname, country, function () {
//            $scope.players.push({username: username, team_name: team_name});
            $scope.status = "Successfully edited player " + username;
        }, function () {
            $scope.status = "Error editing player";
        });
    };

    $scope.saveAvatar = function (data) {
        var player_id = parseInt($routeParams.playerId);
        var username = $scope.player.data[0].username;
        var team_id = $scope.player.data[0].team_id;
        var avatar = data;
        var realname = $scope.player.data[0].realname;
        var country = $scope.player.data[0].countrycode;
        daoPlayers.edit(player_id, username, team_id, avatar, realname, country, function () {
//            $scope.players.push({username: username, team_name: team_name});
            $scope.status = "Successfully edited player " + username;
        }, function () {
            $scope.status = "Error editing player";
        });
    };

    $scope.saveRealname = function (data) {
        var player_id = parseInt($routeParams.playerId);
        var username = $scope.player.data[0].username;
        var team_id = $scope.player.data[0].team_id;
        var avatar = $scope.player.data[0].avatar;
        var realname = data;
        var country = $scope.player.data[0].countrycode;
        daoPlayers.edit(player_id, username, team_id, avatar, realname, country, function () {
//            $scope.players.push({username: username, team_name: team_name});
            $scope.status = "Successfully edited player " + username;
        }, function () {
            $scope.status = "Error editing player";
        });
    };

});

