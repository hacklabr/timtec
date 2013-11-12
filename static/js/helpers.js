RegExp.prototype.extract = function(target,group){
    if(this.test(target)) {
        var m=target.match(this);
        if(group > 0 && group < m.length)
            return m[group];
        return m[0];
    }
};

if(jQuery) {
    jQuery.fn.asArray = function() {
        return Array.prototype.slice.call(this);
    };
}