(function(angular){
    'use strict';

    var app = angular.module('activities', [
      'django',
      'activities.controllers',
      'activities.directives',
      'discussion.directives',
      'ui.bootstrap',
      'ui.codemirror',
      'duScroll',
    ]);

    // Set new default values for 'duScroll'
    app.value('duScrollDuration', 1000);
    app.value('duScrollOffset', 100);

})(angular);
