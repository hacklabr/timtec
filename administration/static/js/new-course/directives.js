(function(angular) {
    'use strict';

    var app = angular.module('new-course');

    app.directive('contenteditable', function(){
        return {
            'restrict': 'A',
            'require': '?ngModel',
            'link': function(scope, element, attrs, ngModel) {
                if(!ngModel) return;
                ngModel.$render = function(){ element.html(ngModel.$viewValue || ''); };
                element.on('blur keyup change', function() { scope.$apply(read); });
                function read() {
                    var html = element.html();
                    if( attrs.stripBr && html.match(/ *<br\/?> */) ){
                        html = '';
                    }
                    ngModel.$setViewValue(html);
                }
            }
        };
    });

    app.directive('markdowneditor', function(){

        var template = ''+
        '<div class="editable" ng-bind="content" ng-click="open()"></div>' +
        '<button class="btn btn-default btn-sm" ng-click="open()" ng-show="!content">Adicionar texto</button>' +
        '<div class="modal fade in" id="Modal" tabindex="-1" ng-style="modalState()">' +
            '<div class="modal-dialog">' +
                '<div class="modal-content">' +
                    '<div class="modal-header">' +
                      '<button type="button" class="close" ng-click="close()">&times;</button>' +
                      '<h4 class="modal-title">{{ title }}&nbsp;</h4>' +
                    '</div>' +
                    '<div class="modal-body">' +
                        '<div class="text-editor">' +
                            '<div class="row">' +
                                '<div class="col-lg-12" id="wmd-button-bar-{{id}}"></div>' +
                            '</div>' +
                            '<div class="row">' +
                                '<div class="col-lg-12 form-group">' +
                                    '<textarea id="wmd-input-{{id}}" class="col-lg-12 form-control" ng-model="content" rows="15"></textarea>' +
                                '</div>' +
                            '</div>' +
                        '</div>' +
                        '<div class="modal-footer">' +
                            '<button type="button" class="btn btn-default" ng-click="close()">Cancelar</button>' +
                            '<button type="button" class="btn btn-primary">Save changes</button>' +
                        '</div>' +
                    '</div>' +
                '</div>' +
            '</div>' +
        '</div>';

        return {
            'restrict': 'E',
            'template': template,
            'scope': {
                'content': '=',
                'title': '='
            },
            'controller': function($scope) {
                $scope.active = false;
                $scope.id = Math.random().toString(16).slice(2);
                $scope.modalState = function(){ return {display: $scope.active?'block':'none'}; };
                $scope.close = function() { $scope.active = false; };

                var running = false;
                var editor = new window.Markdown.Editor(
                    window.Markdown.getSanitizingConverter(), '-'.concat($scope.id)
                );

                $scope.open = function() {
                    $scope.active = true;
                    if ( !running ) {
                        editor.run();
                    }
                    running = true;
                };
            },
            'link': function(scope, element, attr) {
            }
        };
    });

})(window.angular);