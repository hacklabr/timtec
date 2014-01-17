(function(angular) {
    'use strict';

    var app = angular.module('directive.alertPopup', []);

    app.directive('alertPopup', function(){
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
})(window.angular);
