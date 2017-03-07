(function ($) {
    $(document).ready(function ($) {
        var rs = $("input[id*='is_default']");
        for (var i = 0; i < rs.length; i++) {
            $(rs[i]).on('click', function (event) {

                var list = $("input[id*='is_default']");
                for (var j = 0; j < list.length; j++) {
                    if (event.currentTarget.id != $(list[j])[0].id) {
                        $(list[j]).removeAttr("checked")
                    }
                }
            });
        }
    });
})(django.jQuery);