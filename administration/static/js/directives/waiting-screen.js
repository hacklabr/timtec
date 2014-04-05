(function(angular) {
    'use strict';

    var app = angular.module('directive.waiting-screen', []);

    app.factory('waitingScreen', [
        '$q',
        function($q){

            var waitingScreen = { };
            var elementDefer = $q.defer();
            var elementResolved = false;

            elementDefer.promise.then(function(){
                elementResolved = true;
            });

            waitingScreen.setElement = function(element){
                element.remove();

                if(!elementResolved) {
                    element.appendTo(document.body);
                    elementDefer.resolve(element);
                }
            };

            waitingScreen.hide = function() {
                elementDefer.promise.then(function(element) {
                    element.hide(0);
                });
            };

            waitingScreen.show = function() {
                elementDefer.promise.then(function(element) {
                    element.show(0);
                });
            };

            return waitingScreen;
        }
    ]);

    app.directive('waitingScreen', [
        'waitingScreen',

        function(waitingScreen){
            return {
                'restrict': 'A',
                'link': function(scope, element, attrs, ngModel) {
                    waitingScreen.setElement(element);
                }
            };
        }
    ]);

})(window.angular);
