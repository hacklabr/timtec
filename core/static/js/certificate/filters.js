
(function (angular) {
    'use strict';

    var module = angular.module('certification');

    module.filter('attending', function() {
        return function (items, evaluation_id){
            if(!items || !evaluation_id) return;
            var filtered = [];
            for (var i = 0; i < items.length; i++) {
                // console.log(items[i].klass);
                if (evaluation_id == items[i].evaluation) filtered.push(items[i]);
            }
            return filtered;
        }
    });

    module.filter('can_attend', function(){
        return function (items){
            if(!items) return;
            var filtered = [];
            for (var i = 0; i < items.length; i++) {
                if (!items[i].evaluation && items[i].course_certification)
                    filtered.push(items[i]);
            }
            return filtered;
        }
    });


})(angular);
