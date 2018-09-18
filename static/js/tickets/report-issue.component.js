(function () {
    "use strict";
    angular
        .module('ticket')
        .component('reportIssue', {
            'templateUrl': 'static/html/report-issue.template.html',
            'controller': ['$window', '$routeParams', '$location', '$http',
                           function ($window, $routeParams, $location, $http) {
                var self = this;
                var ticketId = $routeParams.ticketId;

                this.statusOptions = {'Backlog': 'backlog', 'Selected for Development': 'selected for development',
                                    'In progress': 'in progress', 'Ready for release': 'ready for release',
                                    'Done': 'done'};
                this.typeOptions = {'Trivial': 'trivial', 'Minor': 'minor', 'Major':'major',
                                    'Critical': 'critical', 'Blocker': 'blocker'};

                this.createIssue = function () {
                    var data = {'title': this.title, 'description': this.description,
                                'status': this.status, 'type': this.type, 'tags': this.tags}
                    $http({
                        url: 'tickets/',
                        method: "POST",
                        data: data,
                    }).then(function successCallback(response) {
                        self.tickets = response.data;
                        $location.path('my-tickets/');
                    }, function failureCallback(response) {
                        self.errors = response.data;
                    })
                };
            }]
        });
}());
