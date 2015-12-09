(function(angular){
    'use strict';
    var app = angular.module('profile');


    app.controller('UserCertificatesController',
        ['$scope', '$modal', 'CourseCertificationService'
        function ($scope, $modal, CourseCertification) {
            $scope.student_certificate_list = CourseCertificationService.get();

        }
    ]);

})(window.angular);