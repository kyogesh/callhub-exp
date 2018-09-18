(function () {
    "use strict";
    angular
        .module("auth")
        .factory("AuthService", ["$http", '$cookies', function ($http, $cookies) {
            var user = {};
            var loggedIn = $cookies.getObject('loggedIn');
            if (loggedIn === undefined) {
                user.loggedIn = false;
            }
            else {
                user.loggedIn = true;
                user.loggedUsername = $cookies.get('loggedUsername');
            }

            var asyncLogin = function (username, password) {
                var data = { 'username': username, 'password': password };
                // Authorization header isn't required on get-token endpoint
                var config = { 'headers': { 'Authorization': undefined } };
                return $http.post("user/get-token/", data, config).then(
                    function successCallback(response) {
                        // Api doesn't return the username. So we have to add it here to keep track of it in the service
                        response.data.username = username;
                        _login(response.data);
                        return {'status': response.status, 'errors': null};
                    },
                    function errorCallback(response) {
                        return {'status': response.status, 'errors': response.data};
                    });
            };

            var _login = function (data) {
                $cookies.putObject('loggedIn', true);
                $cookies.put('loggedUsername', data.username);
                $cookies.put('token', data.token);

                // Set user attributes
                user.loggedUsername = $cookies.get('loggedUsername');
                user.loggedIn = true;
            };

            var logout = function () {
                $cookies.remove('loggedIn');
                $cookies.remove('loggedUsername');
                $cookies.remove('token');

                // Unset user attributes
                user.loggedIn = false;
                delete user.loggedUsername;
            };

            var updatePassword = function (data){
                return  $http.post("user/change_password/", data).then(function (response) {
                            return response.status;
                         });
            };

            return {
                'logout': logout,
                'user': user,
                'asyncLogin': asyncLogin,
                // Only exposing _login so it could be tested.
                // Controllers shoudn't be using this service function.
                '_login': _login,
                'updatePassword': updatePassword,
            };
        }]);
}());
