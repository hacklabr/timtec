(function(angular){
    'use strict';

    angular.module('core', [
        'core.controllers',
        'core.services',
        'ngResource',
        'django',
        'twitterFilters',
        'ui.bootstrap',
    ]);

})(angular);
