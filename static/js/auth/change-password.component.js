(function () {
    "use strict";
    angular
        .module("auth")
        .component("changePassword", {
            "templateUrl": "static/html/change-password.template.html",
            "controller": ['$location', 'AuthService', function ($location, AuthService) {
                var self = this;
                this.changePassword = function (){
                   if (self.password == self.confirmPassword){
                        updatePassword();
                   }
                   else{
                        self.errors = "Passwords don't match!";
                   }
                };

                var updatePassword = function(){
                    var data = {'password': self.password};
                    AuthService.updatePassword(data).then(function (status) {
                        if(status == 200){
                            AuthService.logout();
                            $location.path('/login');
                        }
                        else{
                        self.errors = "Enter Valid Password";
                        }
                    });
                };
            }]
        });
}());
