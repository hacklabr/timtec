(function(angular) {
    'use strict';

    var app = angular.module('directive.sortable', []);

    app.directive('sortable', function(){
        return {
            'restrict': 'A',
            'scope': {
                'list': '=sortable',
                'onUpdate': '&onUpdate'
            },
            'link': function(scope, element) {
                var startIdx;

                function start(evt, o) {
                    startIdx = jQuery(o.item).index();
                    console.log();
                }

                function update(evt, o) {
                    var endIdx = jQuery(o.item).index();

                    if (startIdx === endIdx) return;

                    var item = scope.list.splice(startIdx, 1);
                    var tail = scope.list.splice(endIdx);

                    // we need to hold referece to original scope.list
                    // do not assign anything directly in scope.list
                    item.concat(tail).forEach(function(el){
                        scope.list.push(el);
                    });

                    if(scope.onUpdate && scope.onUpdate.call) {
                        scope.onUpdate.call();
                    }
                }

                element.sortable({
                    'handle': '.handle',
                    'update': update,
                    'start': start
                });

            }
        };
    });
})(window.angular);
