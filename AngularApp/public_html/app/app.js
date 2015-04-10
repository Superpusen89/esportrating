var app = angular.module('clientApp', ['ngRoute', 'xeditable', 'ui.bootstrap']);

app.config(function($routeProvider) {
  $routeProvider
          .when('/players', {
            controller: 'PlayersController',
            templateUrl: 'app/partials/players.html'
          })
          .when('/player/:playerId', {
            controller: 'PlayerController',
            templateUrl: 'app/partials/player.html'
          })
          .otherwise({redirectTo: '/players'});
});

app.constant('REST', {
  'path': 'http://0.0.0.0:5001/'
});