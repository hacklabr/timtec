
(function() {
    "use strict";

    CodeMirror.commands.autocomplete = function(cm) {
        CodeMirror.showHint(cm, CodeMirror.hint.html);
    };

    window.CodeMirrorConf = {
        lineNumbers:true,
        theme:"monokai",
        matchTags: {bothTags: true},
        matchBrackets: true,
        extraKeys: {"Ctrl-J": "toMatchingTag",
                    "Ctrl-Space": "autocomplete"},
        mode:"htmlmixed"
    };
})();
