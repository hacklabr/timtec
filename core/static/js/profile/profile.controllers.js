(function(angular){
    'use strict';
    var app = angular.module('profile.controllers', ['ngSanitize']);

        function ($scope, $location, TimtecUser, CurrentUser) {

            // remove the last slash
            var abs_url = $location.absUrl();
            if (abs_url.slice(-1) === '/') {
                abs_url = abs_url.slice(0, -1);
            }

            var username = abs_url.split('/').pop();
            $location.absUrl().split('/').indexOf("profile")
            if (username === 'profile' || username === 'edit') {
                // Current user profile
                username = CurrentUser.username;
            }

            TimtecUser.get({username: username}, function(user_profile) {
                user_profile.is_current_user = (user_profile.id === parseInt(CurrentUser.id, 10));
                $scope.user_profile = user_profile;
            }, function(error) {
                $scope.user_profile = null;
            });
        }
    ]);

})(window.angular);
