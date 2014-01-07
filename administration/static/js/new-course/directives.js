(function(angular){
    'use strict';
    var app = angular.module('new-course');

    app.directive('file', function(){
        return {
            'restrict': 'E',
            'require': '?ngModel',
            'link': function(scope, element, attrs, ngModel) {
                var input = document.createElement('input');
                input.type = 'file';
                input.onchange = function(evt) {
                    if(evt.target.files) {
                        ngModel.$setViewValue(evt.target.files[0]);
                    }
                    scope.$apply();
                };

                for( var att in attrs ) {
                    if(! /^ng/.test(att)) {
                        input[att] = element.attr(att);
                    }
                }
                input.className = element.attr('class').replace(/\bng[^ ]+ */g, '').trim();
                element.attr('class', '');

                element.append(input);
            }
        };
    });

    app.directive('localImage', function(){
        return {
            'restrict': 'A',
            'link': function(scope, element, attrs) {
                var img = element[0];
                var reader = new FileReader();

                reader.onload = function(evt) {
                    img.src = evt.target.result;
                };

                if( attrs.ngModel ) {
                    scope.$watch(attrs.ngModel, function(d){
                        if( window.File && d && d.constructor === window.File ) {
                            img.style.display = '';
                            reader.readAsDataURL( d );
                        } else {
                            img.style.display = 'none';
                        }
                    });
                }
            }
        };
    });

    app.directive('alert', function(){
        return {
            'restrict': 'A',
            'link': function(scope) {

                scope.alert = {
                    hidden : true,
                    reset: function(){
                        this.title = '';
                        this.type = '';
                        this.messages = [];
                        this.showControls=false;
                    },
                    popup: function(title, messages, showControls){
                        this.reset();
                        this.title = title;
                        this.messages = messages;
                        this.showControls = showControls;
                        this.hidden = false;
                    },
                    success: function(){
                        this.popup.apply(this, arguments);
                        this.type = 'success';
                        this.hide(null, 1000);
                    },
                    error: function(){
                        this.popup.apply(this, arguments);
                        this.type = 'danger';
                    },
                    warn: function(){
                        this.popup.apply(this, arguments);
                        this.type = 'warning';
                    },
                    hide: function(callback, timeout) {
                        var that = this;
                        setTimeout(function(){
                            that.hidden = true;
                            if(callback && callback.call)
                                callback.call();
                            scope.$apply();
                        }, timeout || 3000);
                    }
                };
                scope.alert.reset();
            }
        };
    });

    app.directive('professorslist', ['Professor', function(Professor){
        function noop(){ }

        return {
            'restrict': 'E',
            'templateUrl': '/static/templates/directive.professorslist.html',
            'scope': {
                'active': '=',
                'onSelect': '='
            },
            'controller': ['$scope', function($scope){
                $scope.professors = Professor.query();
                $scope.selectedProfessor = null;

                $scope.selectProfessor = function() {
                    if(!$scope.selectedProfessor) return;

                    if($scope.onSelect && $scope.onSelect.call) {
                        $scope.onSelect($scope.selectedProfessor);
                    }
                };
            }]
        };
    }]);

    app.directive('fixedBar', function() {
        return {
            'restrict': 'A',
            'link': function(scope, el) {
                var parent = el.parent();

                var barOffsetTop = el.offset().top;
                var barHeight = parseInt(el.css('height'), 10);
                var barMarginTop = parseInt(el.css('marginTop'), 10);
                var barAbsMarginTop = Math.abs(barMarginTop);

                var preparedHeight = barHeight + barAbsMarginTop + 'px';
                var preparedTop = barAbsMarginTop + 'px';

                window.onscroll = function() {
                    if (window.scrollY >= barOffsetTop) {
                        parent.css('margin-top', preparedHeight);
                        el.css('left', '0');
                        el.css('position', 'fixed');
                        el.css('right', '0');
                        el.css('top', preparedTop);
                        el.css('z-index', 1000);
                    } else {
                        parent.css('margin-top', '');
                        el.css('position', '');
                        el.css('top', '');
                        el.css('z-index', '');
                    }
                };
            }
        };
    });

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