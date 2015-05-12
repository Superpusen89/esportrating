var app = angular.module('clientApp', ['ngRoute', 'xeditable', 'ui.bootstrap']); /* 'ngResource', 'ngProgress' */

webshims.setOptions('forms-ext', {types: 'date'});
webshims.polyfill('forms forms-ext');

app.config(function ($routeProvider) {
    $routeProvider
            .when('/players', {
                controller: 'PlayersController',
                templateUrl: 'app/partials/players.html'
            })
            .when('/player/:playerId', {
                controller: 'PlayerController',
                templateUrl: 'app/partials/player.html'
            })
            .when('/tournaments', {
                controller: 'TournamentsController',
                templateUrl: 'app/partials/tournaments.html'
            })
            .when('/tournament/:tournamentId', {
                controller: 'TournamentController',
                templateUrl: 'app/partials/tournament.html'
            })
            .when('/matches', {
                controller: 'MatchesController',
                templateUrl: 'app/partials/matches.html'
            })
            .when('/match/:matchId', {
                controller: 'MatchController',
                templateUrl: 'app/partials/match.html'
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
            .when('/team/:teamId', {
                controller: 'TeamController',
                templateUrl: 'app/partials/team.html'
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


