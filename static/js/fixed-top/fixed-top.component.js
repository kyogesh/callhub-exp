(function () {
    "use strict";
    angular
        .module('fixedTop')
        .component('fixedTop', {
            'templateUrl': 'static/html/fixed-top.template.html',
            'controller': ['AuthService', '$location', '$window', function (AuthService, $location,  $window) {
                this.user = AuthService.user;
                this.logout = function () {
                    AuthService.logout();
                    $location.path('/login');
                };
            }]
        });
}());
