(function () {
    "use strict";
    angular
        .module('tags')
        .component('search', {
            'templateUrl': 'static/html/search.template.html',
            'controller': ['$window', '$http', function ($window, $http) {
                var self = this;
                this.search = function(searchText) {
                    $http({url:'search/', method:'POST', data:{search_text:searchText}}
                        ).then(function successCallback(response) {
                            self.tickets = response.data;
                        });
                }

            }]
        });
}());
