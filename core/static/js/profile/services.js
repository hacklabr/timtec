(function (angular) {
    'use strict';

    var module = angular.module('profile');

    module.service('CourseCertificationService',
    ['CourseCertification', function (CourseCertification){
            var course_certification = CourseCertification.query(function (cc){
                return cc;
            });
            return {
                'get' : function(){
                    return course_certification;
                }
            };
        }
    ]);
})(angular);
