function argsLog () {
    if(console.log) {
        console.log.apply(console, arguments);
    }
    return arguments;
}

RegExp.prototype.extract = function(target,group){
    if(this.test(target)) {
        var m=target.match(this);
        if(group > 0 && group < m.length)
            return m[group];
        return m[0];
    }
};

String.prototype.format = function () {
    var array;

    if( arguments.length < 1)
        return this.toString();

    function reduce(o1, o2) {
        if(o2.constructor === Array)
            return o1.concat(o2);
        return o1.concat([o2]);
    }

    array = Array.prototype.reduce.call(arguments, reduce, []);

    return this.replace(/\{(\d+)\}/g, function(region, index){
        index = parseInt(index, 10);
        if (index >= array.length) {
            return region;
        }
        return array[index];
    });
};

(function($) {
    if(!$) return;

    $.fn.notify = function(text, clazz) {
        var $div = $('<div style="width:100%;position:fixed;bottom:2em;z-index:1051;text-align:center;">');
        var $span = $('<span class="alert">').addClass(clazz).html(text);
        $div.append($span);
        $(this).css('position','relative').append($div);
        setTimeout(function(){ $div.remove(); }, 5000);
    };

    $.fn.asyncSubmit = function() {
        var $this = $(this);
        var action = $this.attr('action');
        var method = $this.attr('method');

        var data = {};
        $this.find(':input').each(function(i,e){
            data[ $(e).attr('name') ] = $(e).val();
        });

        var request = $.ajax({
            url: action,
            type: method,
            data: data
        });
        return request;
    };
})(jQuery);
