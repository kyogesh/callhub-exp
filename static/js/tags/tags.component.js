(function () {
    "use strict";
    angular
        .module('tags')
        .component('tags', {
            'templateUrl': 'static/html/home.template.html',
            'controller': ['$window', '$routeParams', '$http', function ($window, $routeParams, $http) {
                var self = this;
                var tag = $routeParams.tag;
                var url = 'tickets-with-tag/'+ tag + '/'
                $http.get(url).then(function successCallback(response) {
                    self.tickets = response.data;
                })

            }]
        });
}());
