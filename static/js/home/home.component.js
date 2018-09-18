(function () {
    "use strict";
    angular
        .module('home')
        .component('home', {
            'templateUrl': 'static/html/home.template.html',
            'controller': ['$window', '$http', function ($window, $http) {
                self = this;
                $http.get('tickets/').then(function successCallback(response) {
                    self.tickets = response.data;
                })

            }]
        });
}());
