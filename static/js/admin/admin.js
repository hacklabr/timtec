(function(angular){
  "use strict";

  var app = angular.module('admin', ['ngRoute', 'ngResource', 'youtube']);

  app.controller('CourseEdit',['$scope',
    function($scope){
      $scope.form = {
        "abstract": "",
        "application": "",
        "intro_video": "",
        "name": "",
        "professors": [],
        "pronatec": "",
        "publication": "",
        "requirement": "",
        "slug": "",
        "status": "",
        "structure": "",
        "students": "",
        "workload": ""
      };
    }
  ]);

})(angular);