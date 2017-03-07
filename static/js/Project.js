// var i = 0;
// function setbar() {
//     console.log("setbar");
//     i += 5;
//     if (i >= 105) {
//         clearInterval(showbar);
//     }
//     document.getElementById("bar").style.width = i + "%";
//     document.getElementById("bar").innerHTML = i + "%";
// }

(function ($) {

    // function startbar() {
    //     var showbar = setInterval("setbar()", 1000);
    // }


    // $(document).ready(function ($) {
    //     var i = 0;
    //     $('table tr').each(function () {
    //         if (i == 0) {
    //             var trHtml = "<th style='width: 15%'>状态</th>";
    //             $(this).append(trHtml);
    //         }
    //         if (i != 0 && this.children.length > 2) {
    //             var trHtml = "<td style='width: 15%'><div cla> <span id='bar' style='width: 10%;'>10%</span>  </div></td>";
    //             $(this).append(trHtml);
    //
    //         }
    //         i++;
    //     });
    //
    // });

    $(document).ready(function () {
        $(".extra_btn-column").attr("width", "15%");
    });


})(django.jQuery);