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
                templateUrl: 'app/partials/playersView.html'
            })
            .when('/editPlayers', {
                controller: 'PlayersController',
                templateUrl: 'app/partials/editPlayersView.html'
            })
            .when('/player/:playerId', {
                controller: 'PlayerController',
                templateUrl: 'app/partials/playerView.html'
            })
            .when('/editPlayer/:playerId', {
                controller: 'PlayerController',
                templateUrl: 'app/partials/editPlayerView.html'
            })
            .when('/tournaments', {
                controller: 'TournamentsController',
                templateUrl: 'app/partials/tournamentsView.html'
            })
            .when('/editTournaments', {
                controller: 'TournamentsController',
                templateUrl: 'app/partials/editTournamentsView.html'
            })
            .when('/tournament/:tournamentId', {
                controller: 'TournamentController',
                templateUrl: 'app/partials/tournamentView.html'
            })
            .when('/editTournament/:tournamentId', {
                controller: 'TournamentController',
                templateUrl: 'app/partials/editTournamentView.html'
            })
            .when('/addTournament', {
                controller: 'AddTournamentController',
                templateUrl: 'app/partials/addTournamentView.html'
            })
            .when('/matches', {
                controller: 'MatchesController',
                templateUrl: 'app/partials/matchesView.html'
            })
            .when('/editMatches', {
                controller: 'MatchesController',
                templateUrl: 'app/partials/editMatchesView.html'
            })
            .when('/match/:matchId', {
                controller: 'MatchController',
                templateUrl: 'app/partials/matchView.html'
            })
            .when('/editMatch/:matchId', {
                controller: 'MatchController',
                templateUrl: 'app/partials/editMatchView.html'
            })
            .when('/addMatch', {
                controller: 'AddMatchController',
                templateUrl: 'app/partials/addMatchView.html'
            })
            .when('/login', {
                templateUrl: 'app/partials/loginView.html'
            })
            .when('/teams', {
                controller: 'TeamsController',
                templateUrl: 'app/partials/teamsView.html'
            })
            .when('/editTeams', {
                controller: 'TeamsController',
                templateUrl: 'app/partials/editTeamsView.html'
            })
            .when('/team/:teamId', {
                controller: 'TeamController',
                templateUrl: 'app/partials/teamView.html'
            })
            .when('/editTeam/:teamId', {
                controller: 'TeamController',
                templateUrl: 'app/partials/editTeamView.html'
            })
            .when('/addTeam', {
                controller: 'AddTeamController',
                templateUrl: 'app/partials/addTeamView.html'
            })
            .when('/addPlayer', {
                controller: 'AddPlayerController',
                templateUrl: 'app/partials/addPlayerView.html'
            })
            .otherwise({redirectTo: '/players'});
});

app.constant('REST', {
    'path': 'http://0.0.0.0:5001/'
});


