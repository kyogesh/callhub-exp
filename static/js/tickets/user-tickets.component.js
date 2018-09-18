(function () {
    "use strict";
    angular
        .module('ticket')
        .component('userTicket', {
            'templateUrl': 'static/html/user-tickets.template.html',
            'controller': ['$window', '$routeParams', '$http', function ($window, $routeParams, $http) {
                var self = this;
                var ticketId = $routeParams.ticketId;
                $http.get('user-tickets/').then(function successCallback(response) {
                    self.tickets = response.data;
                })
                this.selectTicket = function (ticket) {
                    self.selectedTicket = ticket;
                 };
            }]
        });
}());
