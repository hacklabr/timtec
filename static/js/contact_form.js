/** require helpers.js */

(function($){
    $(function(){
        $('#modal-contact form:first').submit(function(evt){
            var $this = $(this);
            evt.preventDefault();

            $this.asyncSubmit().fail(function(){
                $this.addClass('.has-error');
                $(document.body).notify('Mensagem não enviada!', 'alert-danger');
            }).done(function(){
                $this.removeClass('.has-error');
                $('#modal-contact').modal('hide');
                $(document.body).notify('Mensagem enviada!', 'alert-success');
            });
            return false;
        });
    });
})(jQuery);