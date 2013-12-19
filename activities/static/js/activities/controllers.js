(function(angular){
    'use strict';

    var app = angular.module('activities.controllers', ['ui.codemirror']);

    app.controller('HTML5Ctrl',
        function ($scope) {
            $scope.codemirrorLoaded = function(cm){

                cm.on("change", function() {
                    cm.markText({line:0, ch:0}, {line:4, ch:0}, {atomic: true, readOnly: true, inclusiveLeft: true});
                    var lastLine = cm.lineCount();
                    alert(lastLine);
                    cm.markText({line:lastLine-3, ch:1000}, {line:lastLine, ch:0}, {atomic: true, readOnly: true, inclusiveRight: true});

                });
              };
        });

})(window.angular);
