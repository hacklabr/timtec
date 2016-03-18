(function(angular){
    'use strict';
    var app = angular.module('profile.controllers', []);

    app.controller('UserProfileController', ['$scope', '$location', 'UserProfile', 'CurrentUser',
        function ($scope, $location, TimtecUser, CurrentUser) {

            // remove the last slash
            var abs_url = $location.absUrl();
            if (abs_url.slice(-1) === '/') {
                abs_url = abs_url.slice(0, -1);
            }

            var username = abs_url.split('/').pop();
            $location.absUrl().split('/').indexOf("profile")
            if (username !== 'profile') {
                $scope.user_profile = TimtecUser.get({username: username});
            } else {
                $scope.user_profile = TimtecUser.get({userId: CurrentUser.id});
            }
        }
    ]);

})(window.angular);
