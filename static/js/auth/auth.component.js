(function () {
    "use strict";
    angular
        .module("auth")
        .component("login", {
            "templateUrl": "static/html/login.template.html",
            "controller": ['$location', '$cookies', 'AuthService', function ($location, $cookies, AuthService) {
                var self = this;
                this.login = function () {
                    AuthService.asyncLogin(this.username, this.password).then(function (response) {
                        if (response.status == 200) {
                            var redirectPath = $cookies.get('requestedUrl');
                            $cookies.remove('requestedUrl');
                            if (!redirectPath || redirectPath == '/login') {
                                $location.path('/');
                            }
                            else {
                                $location.path(redirectPath);
                            }
                        }
                        else {
                            self.errors = 'Invalid Username/Password';
                        }
                    });
                };
            }]
        });
}());
