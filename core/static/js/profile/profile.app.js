(function(angular){
    'use strict';

    angular.module('profile', [
        'profile.controllers',
        'profile.services',
        'django',
        'header',
        'ui.tinymce',
    ]);
})(angular);
