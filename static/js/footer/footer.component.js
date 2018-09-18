(function () {
    "use strict";
    angular
        .module('footer')
        .component('footer', {
            'templateUrl': 'static/html/footer.template.html',
            'controller': ['$window', '$http', function ($window, $http) {
            }]
        });
}());
