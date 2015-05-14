app.controller('AddPlayerController', function ($scope, daoPlayers, daoTeams, daoCountries) {
    $scope.status = "";


    $scope.addPlayer = function () {
        
        $scope.status = "";
                
        var username = $scope.newPlayer.username;
        var team_id = $scope.newPlayer.team_id;
        var avatar = $scope.newPlayer.avatar;
        var real_name = $scope.newPlayer.real_name;
        var country = $scope.newPlayer.country;

        /** check if the team exists **/

        var teamarray = [];
        for (i = 0; i < $scope.teams.length; i++) {
            teamarray.push($scope.teams[i].id);
        }

        var countryarray = [];
        for (i = 0; i < $scope.countries.length; i++) {
            countryarray.push($scope.countries[i].alpha_2);
        }

        var inputTeam = document.getElementById("teamlabel").value;
        var inputCountry = document.getElementById("countrylabel").value; 
        if (($.inArray(team_id, teamarray) !== -1 || inputTeam == null || inputTeam == "") && ($.inArray(country, countryarray) !== -1 || inputCountry == null || inputCountry == "")) {
            console.log("team_id inside thing: " + team_id);
//            

            daoPlayers.add(username, team_id, avatar, real_name, country, function () {
                $scope.status = "Successfully created new Player " + username;
            }, function () {
                $scope.status = "Error creating new Player";
            });
            $scope.newPlayer.username = '';
            $scope.newPlayer.team_id = '';
            $scope.newPlayer.avatar = '';
            $scope.newPlayer.real_name = '';
            $scope.newPlayer.country = '';
        } else {
            if ($.inArray(team_id, teamarray) !== -1 || inputTeam == null || inputTeam == "") {
                console.log("The team exists");
            } else {
                $scope.status += "The team does not exist/you have to chose from the dropdownlist\n";
            }
            if($.inArray(country, countryarray) !== -1){
                console.log("The country exists");
            }else{
                $scope.status += "The country does not exist/you have to chose from the dropdownlist";
            } 
        }
    };

    daoTeams.getAll(function (teams) {
        $scope.teams = teams.data;
        console.log('********************** scope teams' + $scope.teams);
    }, function () {
        console.log('Error loading Teams');
    });

    $scope.formatLabelTeam = function (model) {
        for (var i = 0; i < $scope.teams.length; i++) {
            if (model === $scope.teams[i].id) {
                return $scope.teams[i].id + ' ' + $scope.teams[i].team_name;
            }
        }
    };

//    var x = document.getElementById("teamlabel");
//    x.addEventListener("blur", checkTeam, true);
//
//    function checkTeam() {
//        var data = document.getElementById("teamlabel").value; 
//        console.log("data is " + data);
//        var teamarray = [];
//        for (i = 0; i < $scope.teams.length; i++) {
//            teamarray.push($scope.teams[i].id);
//        }
//
//        if ($.inArray(data, teamarray) !== -1) {
//            $scope.status = "Team is in the list";
//        } else {
//            $scope.status = "Team does not exist";
//        }
//    };

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
});