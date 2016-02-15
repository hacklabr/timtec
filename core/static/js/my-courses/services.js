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

    module.service('CompletedCoursesService', ['CurrentUser', 'CourseCertification',
        function(CurrentUser, CourseCertification){

            this.courses_receipts = [];
            this.courses_certificates = [];
            this.courses_cert_process = [];
            this.completed_courses;

//            this.completed_courses = CourseCertification.query({user: CurrentUser.id}, function(courses_certifications) {
//                courses_certifications.forEach(function(course_certification) {
//                    if (course_certification.processes.length > 0) {
//                        this.courses_cert_process.unshift(course_certification);
//                    } else if (course_certification.type === 'certificate' && course_certification.is_valid) {
//                        this.courses_certificates.unshift(course_certification);
//                    } else if (course_certification.type === 'receipt' && course_certification.is_valid) {
//                        this.courses_receipts.unshift(course_certification);
//                    }
//                })
//            })
        }
    ]);

})(angular);
