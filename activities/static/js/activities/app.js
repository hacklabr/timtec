(function(angular){
    'use strict';

    angular.module('activities', [
      'django',
      'activities.controllers',
      'activities.directives',
      'discussion.directives',
      'ui.bootstrap',
      'ui.codemirror',
    ]);
})(angular);
