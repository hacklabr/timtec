(function(angular){
    'use strict';

    var app = angular.module('php.controllers', []);

    app.controller('PHPCtrl',
        function ($scope) {
            // if( !$scope.answer.given ) {
                // var btemplate = "<!DOCTYPE html>\n<html>\n  <head></head>\n  <body>\n";
                // var atemplate = "\n  </body>\n</html>";
                // $scope.answer.given = [btemplate + $scope.activity.data.data + atemplate];
            // }
// 
            // $scope.codemirrorLoaded = function(cm){
                // cm.on("change", function() {
                    // cm.markText({line:0, ch:0}, {line:4, ch:0}, {atomic: true, readOnly: true, inclusiveLeft: true});
                    // var lastLine = cm.lineCount();
                    // cm.markText({line:lastLine-3, ch:1000}, {line:lastLine, ch:0}, {atomic: true, readOnly: true, inclusiveRight: true});
                // });
            // };
        }
    );

})(angular);
