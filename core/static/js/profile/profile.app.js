(function(angular){
    'use strict';

    angular.module('profile', [
        'profile.controllers',
        'profile.services',
        'djangular',
        'header',
        'ui.bootstrap',
        'ui.tinymce',
    ]);
})(angular);
