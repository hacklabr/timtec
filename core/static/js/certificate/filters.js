
(function (angular) {
    'use strict';

    var module = angular.module('certification');

    module.filter('attending', function() {
        return function (items, evaluation_id, students){
            if(!items || !evaluation_id) return;
            var filtered = [];

            for (var i = 0; i < items.length; i++) {
                if (evaluation_id == items[i].evaluation) {
                    if(!items[i].student.id){
                        (function(j){
                            items[i].student = students.filter(function(s){return s.id == j;})[0];
                        })(items[i].student);
                    }
                    filtered.push(items[i]);
                }
            }
            return filtered;
        };
    });

    module.filter('can_attend', function(){
        return function (items, students){
            if(!items) return;
            var filtered = [];
            for (var i = 0; i < items.length; i++) {
                if (!items[i].evaluation && items[i].course_certification){
                    if(!items[i].student.id){
                        (function(j){
                            items[i].student = students.filter(function(s){return s.id == j;})[0];
                        })(items[i].student)
                    }
                    filtered.push(items[i]);
                }
            }
            return filtered;
        }
    });


})(angular);
