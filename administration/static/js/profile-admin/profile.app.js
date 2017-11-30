(function(angular){
    'use strict';

    angular.module('profile-admin', [
        'profile-admin.controllers',
        'profile-admin.services',
        'djangular',
        'header',
        'ui.bootstrap',
        'ui.tinymce',
    ]);
})(angular);
