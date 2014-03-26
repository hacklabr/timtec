(function(angular){
    'use strict';

    angular.module('core', [
        'core.controllers',
        'core.services',
        'ngResource',
        'django',
        'twitterFilters',
    ]);

})(angular);
