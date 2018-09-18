(function(){
"use strict";
angular
    .module("registration")
    .component("registration", {
        "templateUrl": "static/html/register.template.html",
        "controller": ['$http', '$location', 'AuthService', function($http, $location, AuthService){
            var self = this;
            this.register = function () {
                this.errors ={};
                var self = this;
                if (this.username.indexOf(' ') <= -1 )
                {
                    var data = {'username': this.username, 'password': this.password,
                              'email': this.email, 'first_name': this.first_name,
                              'last_name': this.last_name};
                    var config = { 'headers': { 'Authorization': undefined } };
                    $http.post("user/register/", data, config).then(
                        function successCallback(response) {
                            AuthService.asyncLogin(self.username, self.password).then(function (response) {
                                $location.path('/visualizations/create');
                            });
                        },
                        function errorCallback(response) {
                            if(response.data.hasOwnProperty('username')){
                                    self.errors.username = response.data.username[0];
                            }
                            if(response.data.hasOwnProperty('email')){
                                self.errors.email = response.data.email[0];
                            }
                        });
                }else {
                    this.errors.username = "whitespaces are not allowed";
                }
            };
        }]
    });
}());
