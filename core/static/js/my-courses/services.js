(function (angular) {
    'use strict';

    var module = angular.module('my-courses');

    module.service('CourseStudentService',
    ['CourseStudent', function (CourseStudent){
            var course_student = CourseStudent.query(function (cs){
                return cs;
            });
            return {
                'get' : function(){
                    return course_student;
                }
            };
        }
    ]);
})(angular);
