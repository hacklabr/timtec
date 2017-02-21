(function(angular){
    'use strict';

    angular.module('certification', [
        'django',
        'timtec-models',
        'directive.file',
        'directive.previewImage',
        'directive.alertPopup',
        'directive.fixedBar',
        'ui.bootstrap',
        'truncate',
        'checklist-model',
        'ngRoute',
        'ngResource',
        'header',
    ])
    .config(function($routeProvider, $locationProvider) {
          $routeProvider
           .when('/', {
                templateUrl: 'course-classes.html',
                controller: 'CourseClassesController',
           })
          .when('/class-evaluations/:klassId', {
            templateUrl: 'class-evaluations.html',
            controller: 'ClassEvaluationsController'
          });

          // configure html5 to get links working on jsfiddle
          // $locationProvider.html5Mode(true);
    });

})(angular);
