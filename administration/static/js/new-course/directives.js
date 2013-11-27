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
        /**
         * require: angular
         * require: Markdown
         * require: jQuery
         * require: modernizr
         */
        var template = ''+
        '<div class="editable" id="wmd-preview-{{id}}" ng-click="open()"></div>' +
        '<button class="btn btn-default btn-sm" ng-click="open()" ng-show="!content">Adicionar texto</button>' +
        '<div class="modal fade in" id="Modal" tabindex="-1" ng-style="modalState()">' +
            '<div class="modal-dialog">' +
                '<div class="modal-content">' +
                    '<div class="modal-header">' +
                      '<button type="button" class="close" ng-click="cancel()">&times;</button>' +
                      '<h4 class="modal-title">{{title}}&nbsp;</h4>' +
                    '</div>' +
                    '<div class="modal-body">' +
                        '<div class="text-editor">' +
                            '<div class="row">' +
                                '<div class="col-lg-12" id="wmd-button-bar-{{id}}"></div>' +
                            '</div>' +
                            '<div class="row">' +
                                '<div class="col-lg-12 form-group">' +
                                    '<textarea id="wmd-input-{{id}}" class="col-lg-12 form-control" ng-model="newContent" rows="15"></textarea>' +
                                '</div>' +
                            '</div>' +
                        '</div>' +
                        '<div class="modal-footer">' +
                            '<button type="button" class="btn btn-default" ng-click="cancel()">Cancelar</button>' +
                            '<button type="button" class="btn btn-primary" ng-click="save()">Save changes</button>' +
                        '</div>' +
                    '</div>' +
                '</div>' +
            '</div>' +
        '</div>';

        return {
            'restrict': 'E',
            'template': template,
            'scope': {
                'content': '=content',
                'onSave': '=onSave'
            },
            'controller': function($scope) {
                $scope.active = false;
                $scope.id = Math.random().toString(16).slice(2);
                $scope.newContent = angular.copy($scope.content);


                $scope.modalState = function(){
                    return {display: $scope.active ? 'block' : 'none'};
                };

                $scope.close = function() {
                    $scope.active = false;
                };

                $scope.open = function() {
                    $scope.active = true;
                };

                $scope.cancel = function() {
                    $scope.newContent = angular.copy($scope.content);
                    $scope.close();
                    $scope.refreshPreview();
                };

                $scope.save = function() {
                    var oldContent = angular.copy($scope.content);
                    $scope.content = angular.copy($scope.newContent);
                    $scope.close();

                    if($scope.onSave && $scope.onSave.call) {
                        try{
                            $scope.onSave();
                        } catch (e) {
                            $scope.content = oldContent;
                            $scope.newContent = oldContent;
                            $scope.refreshPreview();
                            throw e;
                        }
                    }
                };

                $scope.refreshPreview = function() {
                    setTimeout(function(){
                        $scope.editor.refreshPreview();
                    }, 50);
                };

            },
            'link': function(scope, element, attr) {
                var editorIsRunning = false;
                scope.editor = new window.Markdown.Editor(
                    window.Markdown.getSanitizingConverter(), '-'.concat(scope.id)
                );

                scope.$watch('$scope', function(){
                    if(!editorIsRunning) scope.editor.run();
                    editorIsRunning = true;
                });
                scope.title = attr.title;
            }
        };
    });

})(window.angular);