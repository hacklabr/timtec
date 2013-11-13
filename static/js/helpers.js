RegExp.prototype.extract = function(target,group){
    if(this.test(target)) {
        var m=target.match(this);
        if(group > 0 && group < m.length)
            return m[group];
        return m[0];
    }
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

    $.fn.asyncSubmit = function(evt) {
        var $this = $(this);
        var action = $(this).attr('action');
        var method = $(this).attr('method');

        var data = {};
        $(this).find(':input').each(function(i,e){
            data[ $(e).attr('name') ] = $(e).val();
        });

        request = $.ajax({
          url: action,
          type: method,
          data: data
        });
        return request;
    };
})(jQuery);