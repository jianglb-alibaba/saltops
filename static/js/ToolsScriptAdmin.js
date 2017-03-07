(function ($) {
    $(document).ready(function ($) {
        $('.inline_label').remove()
        $('#toolsscript_form').append("<input type='text' style='display: none' id='action' name='action' value='0'></input>")
        $('.submit-row').before("<button  type='submit'  class='btn btn-high'>执行工具</button>")
        sls_host = $('.field-hosts')[0].children[0].children[1].children[0].children[0]
        for (var i = 0; i < $(sls_host)[0].options.length; i++) {
            $(sls_host)[0].options[i].selected = false
        }

        $('#id_toolsexecjob_set-0-param').val("")

        addEventTest($("#toolsscript_form")[0], "submit", function () {
            document.getElementById("action").value = 1;
        });
    });
})
(django.jQuery);

function addEventTest(elem, type, handle) {
    if (elem.addEventListener)
        elem.addEventListener(type, handle, false);
    else if (elem.attachEvent)
        elem.attachEvent("on" + type, handle);
}
function setValue() {
    document.getElementById("action").value = 1;
    document.getElementById("toolsscript_form").submit();
}
