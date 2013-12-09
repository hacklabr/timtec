(function(angular){
    'use strict';
    var app = angular.module('filters.text', []);

    app.filter('slugify', function() {
        return function(text) {
            if ( text && text.constructor === String && text.length > 0 ) {
                return text.toLocaleLowerCase()
                           .trim()
                           .replace(/[àáâãäå]/g,'a')
                           .replace(/ç/g,'c')
                           .replace(/[èéêë]/g,'e')
                           .replace(/[ìíîï]/g,'i')
                           .replace(/ñ/g,'n')
                           .replace(/[òóôõö]/g,'o')
                           .replace(/[ùúûü]/g,'u')
                           .replace(/[ýÿ]/g,'y')
                           .replace(/[^\w\s-]/g, '')
                           .replace(/[-\s]+/g, '-');
            }
            return '';
        };
    });

})(window.angular);