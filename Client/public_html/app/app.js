/*
 * 
 * following code taken from 
 * http://stackoverflow.com/questions/18344569/setting-ng-href-in-tr-elements/23699554#23699554
 */

var app = angular.module('clientApp', ['ngRoute', 'xeditable', 'ui.bootstrap']) 
.directive('suchHref', ['$location', function ($location) {
  return{
    restrict: 'A',
    link: function (scope, element, attr) {
      element.attr('style', 'cursor:pointer');
      element.on('click', function(){
        $location.path(attr.suchHref)
        scope.$apply();
      });
    }
  }
}])
;

/*
 * code end
 */

//webshims.setOptions('forms-ext', {types: 'date'});
//webshims.polyfill('forms forms-ext');

app.config(function ($routeProvider) {
    $routeProvider
            .when('/players', {
                controller: 'PlayersController',
                templateUrl: 'app/partials/players.html'
            })
            .when('/editPlayers', {
                controller: 'PlayersController',
                templateUrl: 'app/partials/editPlayers.html'
            })
            .when('/player/:playerId', {
                controller: 'PlayerController',
                templateUrl: 'app/partials/player.html'
            })
            .when('/editPlayer/:playerId', {
                controller: 'PlayerController',
                templateUrl: 'app/partials/editPlayer.html'
            })
            .when('/tournaments', {
                controller: 'TournamentsController',
                templateUrl: 'app/partials/tournaments.html'
            })
            .when('/editTournaments', {
                controller: 'TournamentsController',
                templateUrl: 'app/partials/editTournaments.html'
            })
            .when('/tournament/:tournamentId', {
                controller: 'TournamentController',
                templateUrl: 'app/partials/tournament.html'
            })
            .when('/editTournament/:tournamentId', {
                controller: 'TournamentController',
                templateUrl: 'app/partials/editTournament.html'
            })
            .when('/addTournament', {
                controller: 'AddTournamentController',
                templateUrl: 'app/partials/addTournament.html'
            })
            .when('/matches', {
                controller: 'MatchesController',
                templateUrl: 'app/partials/matches.html'
            })
            .when('/editMatches', {
                controller: 'MatchesController',
                templateUrl: 'app/partials/editMatches.html'
            })
            .when('/match/:matchId', {
                controller: 'MatchController',
                templateUrl: 'app/partials/match.html'
            })
            .when('/editMatch/:matchId', {
                controller: 'MatchController',
                templateUrl: 'app/partials/editMatch.html'
            })
            .when('/addMatch', {
                controller: 'AddMatchController',
                templateUrl: 'app/partials/addMatch.html'
            })
            .when('/login', {
                templateUrl: 'app/partials/login.html'
            })
            .when('/teams', {
                controller: 'TeamsController',
                templateUrl: 'app/partials/teams.html'
            })
            .when('/editTeams', {
                controller: 'TeamsController',
                templateUrl: 'app/partials/editTeams.html'
            })
            .when('/team/:teamId', {
                controller: 'TeamController',
                templateUrl: 'app/partials/team.html'
            })
            .when('/editTeam/:teamId', {
                controller: 'TeamController',
                templateUrl: 'app/partials/editTeam.html'
            })
            .when('/addTeam', {
                controller: 'AddTeamController',
                templateUrl: 'app/partials/addTeam.html'
            })
            .when('/addPlayer', {
                controller: 'AddPlayerController',
                templateUrl: 'app/partials/addPlayer.html'
            })
            .otherwise({redirectTo: '/players'});
});

app.constant('REST', {
    'path': 'http://0.0.0.0:5001/'
});


