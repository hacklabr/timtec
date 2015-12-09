(function (angular) {
    'use strict';

    var module = angular.module('profile');

    module.service('UserProfileService',
    ['UserProfile', function (UserProfile){
            var profile = UserProfile.get(function (profile){
                return profile;
            });
            return {
                'get' : function(){
                    return profile;
                }
            };
        }
    ]);
})(angular);
