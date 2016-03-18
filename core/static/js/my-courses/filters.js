(function (angular) {
    'use strict';

    var module = angular.module('my-courses');
    module.filter('hasProcess', function() {
        return function (items){
            if(!items) return;
            var filtered = [];
            for (var i = 0; i < items.length; i++) {
                var cs = items[i];
                if(cs.certificate){
                    if(cs.certificate.processes.length){
                        filtered.push(items[i]);
                    }
                }
            }
            return filtered;
        }
    });

    module.filter('getProcesses', function(){
        return function (items){
            if(items.length == 0) return;
            var filtered = [];
            for (var i = 0; i < items.length; i++) {
                Array.prototype.push.apply(filtered, items[i].certificate.processes);
            }
            return filtered;
        }
    });

    module.filter('activeProcess', function(){
        return function (items){
            if(items.length == 0) return;
            var filtered = [];
            for (var i = 0; i < items.length; i++) {
                if(items[i].active) {
                    filtered.push(items[i]);
                }
            }
            return filtered;
        }
    });

    module.filter('certificateIssued', function(){
        return function(items){
            if(!items) return;
            var filtered = [];
            for(var i = 0; i < items.length; i++){
                if(items[i].certificate != null && items[i].certificate.type == 'certificate') {
                    filtered.push(items[i]);
                }
            }
            return filtered;
        }
    });

    module.filter('completedCourses', function(){
        return function(items){
            if(!items) return;
            var filtered = [];
            for(var i = 0; i < items.length; i++){
                if(items[i].certificate != null && items[i].certificate.type == 'receipt') {
                    filtered.push(items[i]);
                }
            }
            return filtered;
        }
    });
})(angular);
