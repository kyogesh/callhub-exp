(function () {
    "use strict";
    angular.
    module('callHubExp').
    config(['$locationProvider', '$routeProvider',
        function config($locationProvider, $routeProvider) {
            $locationProvider.hashPrefix('!');

            $routeProvider.
            when('/home', {
                template: '<home></home>'
            }).
            when('/ticket/:ticketId', {
                template: '<ticket></ticket>'
            }).
            when('/about', {
                template: '<about></about>'
            }).
            when('/gallery', {
                template: '<gallery></gallery>'
            }).
            when('/login', {
                template: '<login></login>',
            }).
            when('/report-issue', {
                template: '<report-issue></report-issue>',
            }).
            when('/tag/:tag', {
                template: '<tags></tags>',
            }).
            when('/search/', {
                template: '<search></search>',
            }).
            when('/my-tickets', {
                template: '<user-ticket></user-ticket>',
            }).
            when('/change-password', {
                template: '<change-password></change-password>',
            }).
            when('/register', {
                template: '<registration></registration>',
            }).
            otherwise('/home');
        }
    ]).
    run(['$rootScope', '$http', '$location', '$cookies', function ($rootScope, $http, $location, $cookies) {
            $rootScope.$on('$routeChangeStart', function (event) {
            // Create a list of routes which should be accessible without login
            var path = $location.path();
            var loggedIn = $cookies.get('loggedIn');
            if (path == '/register') {
                $location.path(path);
            }
            else if (!loggedIn) {
                $location.path('/login');
            }
            $http.defaults.headers.common.Authorization = 'Token ' + $cookies.get('token');
            $http.defaults.headers.post['X-CSRFToken'] = $cookies.get('csrftoken');
            $http.defaults.headers.post['xsrfCookieName'] = $cookies.get('csrftoken');
//            $http.defaults.headers.post['xsrfHeaderName'] = $cookies.get('X-CSRFToken');
        });
    }]);
}());
