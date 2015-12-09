(function(angular){
    'use strict';
    var app = angular.module('profile');


    app.controller('UserCertificatesController',
        ['$scope', '$modal', 'UserProfileService',
        function ($scope, $modal, UserProfileService) {
            $scope.user_profile = UserProfileService.get();
        }
    ]);

})(window.angular);