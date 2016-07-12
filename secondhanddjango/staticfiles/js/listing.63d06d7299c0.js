$(document).ready(function() {
        $('a[name=pagination]').click(function(event) {  //on click
            page = $(this).attr("value");
            if (window.location.href.indexOf("?") > -1) {
                if (window.location.href.indexOf("page=") > -1) {
                    parameter = window.location.href.replace(/(page=).*(&?.*)/, '$1' + page + '$2');
                    console.log("#####" + page);
                    console.log("#####" + parameter);
                    $(this).attr("href", parameter);
                } else {
                    parameter = window.location.href.substring(window.location.href.indexOf("?"))
                    $(this).attr("href", parameter + "&page=" + page);
                }
            } else {
                $(this).attr("href", "?page=" + page);
            }
        });
});
