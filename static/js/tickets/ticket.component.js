(function () {
    "use strict";
    angular
        .module('ticket')
        .component('ticket', {
            'templateUrl': 'static/html/ticket-detail.template.html',
            'controller': ['$window', '$routeParams', '$http', function ($window, $routeParams, $http) {
                var self = this;
                var ticketId = $routeParams.ticketId;
                var url = 'ticket/'+ticketId + '/'
                $http.get(url).then(function successCallback(response) {
                    self.ticket = response.data;
                })
            }]
        });
}());
