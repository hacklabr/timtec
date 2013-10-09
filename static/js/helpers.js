RegExp.prototype.extract = function(target,group){
    if(this.test(target)) {
        var m=target.match(this);
        if(group > 0 && group < m.length)
            return m[group];
        return m[0];
    }
};

window.URL = function(u, p) {
    if( this === window ){
        return new arguments.callee(u, p);
    }
    var url = u || "";
    var params = p || {};

    this.toString = function(){
        return url + this.getQueryString();
    };

    this.getQueryString = function(){
        if(!params) return '';

        var qs = '';
        var separator = '?';
        for (var att in params) {
            qs += separator + att + '=' + encodeURIComponent(params[att]);
            separator = '&';
        }
        return qs;
    };
};